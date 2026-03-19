import pdb
from copy import deepcopy
from datetime import datetime, timedelta
from django import forms


class TimeRangeForm(forms.Form):
    """
    **EXPERIMENTAL / PROTOTYPE**

    **⚠️ WARNING: ⚠️**
    This class is **not** a mature, plug-and-play library feature. It is a "stub" or 
    starting point provided for developers who need to build complex data tables. 

    A simple Django form for filtering querysets by a date range.

    **Concept:**
    This form renders two input fields: "Start Date" and "End Date".
    It is primarily designed to work with the `FilterTable` view to provide 
    time-based filtering for lists of objects.

    **Features:**
    - Uses HTML5 `type="date"` widgets, which trigger the browser's native 
      date picker UI (calendar popup).
    - Dynamically accepts `start_date` and `end_date` as direct arguments 
      during initialization, rather than requiring a nested `initial` dictionary.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the form with optional default dates.

        **Logic:**
        Django forms typically expect initial data to be passed in a dictionary 
        called `initial`. This method overrides that behavior to allow you to 
        pass `start_date` and `end_date` directly as kwargs.

        :param start_date: The default value for the start date field.
        :type start_date: datetime.date or str, optional
        :param end_date: The default value for the end date field.
        :type end_date: datetime.date or str, optional
        """
        # Pop any custom initial data from kwargs so they don't confuse the parent class
        start_date = kwargs.get('start_date', None)
        end_date = kwargs.get('end_date', None)
        if 'start_date' in kwargs.keys(): del kwargs['start_date']
        if 'end_date' in kwargs.keys(): del kwargs['end_date']

        # Call the parent class' constructor
        super().__init__(*args, **kwargs)

        # Define the fields dynamically
        # widget=forms.DateInput(attrs={'type': 'date'}) tells Django to render 
        # <input type="date">, enabling the browser's built-in calendar picker.
        self.fields['start_date'] = forms.DateField(initial=start_date, widget=forms.DateInput(attrs={'type': 'date'}))
        self.fields['end_date'] = forms.DateField(initial=end_date, widget=forms.DateInput(attrs={'type': 'date'}))