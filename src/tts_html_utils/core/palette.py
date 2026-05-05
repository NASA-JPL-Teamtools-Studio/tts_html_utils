from abc import ABC

class ColorPalette(ABC):
    NAME = None
    _instance = None

    def __init__(self, colors=None, aliases=None):
        # Use __dict__ to bypass __setattr__ during setup
        self.__dict__['colors'] = colors or {}
        self.__dict__['aliases'] = aliases or {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance
        
    @classmethod
    def __class_getitem__(cls, key):
        """Enable direct class subscription like VisDiffPalette['key']"""
        instance = cls()
        return instance[key]

    def __getattr__(self, name):
        # Essential: Check if the name exists in __dict__ first to avoid loops
        if name in self.colors:
            return self.colors.get(name)
        elif name in self.aliases:
            return self.colors[self.aliases[name]]
        else:
            raise AttributeError(f'No color found for {name} in palette {self.NAME}')
    
    def __setattr__(self, name, value):
        # If you want to keep the logic of storing attributes in the colors dict:
        if 'colors' in self.__dict__:
            self.colors[name] = value
        else:
            # This handles the initial setup if you don't use the __dict__ trick above
            super().__setattr__(name, value)

    def __getitem__(self, name):
        # __getitem__ usually doesn't cause recursion like __getattr__ does,
        # but it's good to keep it consistent.
        if name in self.colors:
            return self.colors.get(name)
        elif name in self.aliases:
            return self.colors[self.aliases[name]]
        else:
            raise KeyError(f'No color found for {name} in palette {self.NAME}')


class VisDiffPalette(ColorPalette):
    NAME = 'Visual Diff Color Palette'
    def __init__(self):
        super().__init__({
                'green': {'background-color': '#95FB95', 'color': '#333333'},
                'blue': {'background-color': '#ADC4DF', 'color': '#333333'},
                'grey': {'background-color': '#BDBEBD', 'color': '#BDBEBD'},
                'red': {'background-color': '#FF614A', 'color': '#333333'},
                'white': {'background-color': '#FFFFF', 'color': '#333333'},
                'error': {'background-color': '#000000', 'color': '#FF614A'}
            }, {
                'insert':            'green',
                'replace':           'blue',
                'delete':            'red',
                'equal':             'white',
                'empty_from_delete': 'grey',
                'empty_from_insert': 'grey',
                'unmatched':         'red',
                'added':             'green',
                'removed':           'red',
                'modified':          'blue',
                'unchanged':         'white'
            }
            )

class EvrPalette(ColorPalette):
    NAME = 'Visual Diff Color Palette'
    def __init__(self):
        super().__init__({
                'DIAGNOSTIC':  {'background-color': '#90ED91', 'color': '#333333'},
                'COMMAND':     {'background-color': '#0D00FF', 'color': '#F1F1F2'},
                'ACTIVITY_LO': {'background-color': '#D3D3D3', 'color': '#333333'},
                'ACTIVITY_HI': {'background-color': '#666666', 'color': '#F1F1F2'},
                'WARNING_LO':  {'background-color': '#F0F001', 'color': '#333333'},
                'WARNING_HI':  {'background-color': '#FEA500', 'color': '#333333'},
                'FATAL':       {'background-color': '#FF5E66', 'color': '#F1F1F2'} ,
                'SIM ERROR':       {'background-color': '#FF5E66', 'color': '#F1F1F2'} 
            }, {}
            )

