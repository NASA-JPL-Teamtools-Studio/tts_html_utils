import pdb
from pathlib import Path

from django.views.generic import ListView
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime, timedelta
from tts_html_utils.django.forms.time_range_form import TimeRangeForm

TEMPLATE_DIR = Path(__file__).parent.parent.joinpath('templates/filter_table')

class FilterTable(ListView):
    """
    **EXPERIMENTAL / PROTOTYPE**

    A custom Django ListView designed to handle sorting, filtering, and pagination 
    via AJAX without requiring a full page reload.

    **⚠️ WARNING: ⚠️**
    This class is **not** a mature, plug-and-play library feature. It is a "stub" or 
    starting point provided for developers who need to build complex data tables. 
    
    It makes several assumptions (e.g., that you will access data via `__dict__`, 
    which fails for properties or related fields) that you will likely need to 
    override or fix in your subclass.

    **How to use (at your own risk):**
    1. Subclass this view.
    2. Define `model = MyModel`.
    3. Define `columns = [('field_name', True), ('other_field', False)]` (where boolean is 'include_filter').
    4. Define `default_sort`.
    
    **Features provided (stubbed):**
    - **Date Range Filtering:** If `calendar_filter` is set to a field name (e.g., 'created_at').
    - **Column Sorting:** Handles `sortKeys` and `sortDirections` from GET requests.
    - **AJAX Rendering:** Detects `XMLHttpRequest` and returns JSON partials instead of full HTML.
    """
    table_template = str(TEMPLATE_DIR.joinpath('filter_table.html'))
    #TO DO: rename list_table_template to something more sensible
    list_table_template = str(TEMPLATE_DIR.joinpath('filter_table_rows.html'))
    pagination_template = str(TEMPLATE_DIR.joinpath('pagination.html'))
    js_template = str(TEMPLATE_DIR.joinpath('javascript.html'))
    calendar_filter = None
    
    def get_queryset(self):
        """
        Filters and sorts the data based on the URL parameters (GET request).

        **Logic Flow:**
        1. **Date Filtering:** If `self.calendar_filter` is set, checks `start_date` and `end_date`.
        2. **Column Filtering:** Iterates through `self.columns`. If a column name appears in the GET params, adds an `icontains` filter.
        3. **Sorting:** Checks `sortKeys` (comma-separated). Applies descending order if `sortDirections` says 'descending'.

        **Note:** This relies on strict naming conventions (e.g. GET param 'my-field' maps to model field 'my_field').
        """
        queryset = super().get_queryset()

        if self.calendar_filter is not None:
            start_date = self.request.GET.get('start_date')
            end_date = self.request.GET.get('end_date')

            if start_date is not None:
                queryset = queryset.filter(**{f'{self.calendar_filter}__gte':start_date})
            if end_date is not None:
                queryset = queryset.filter(**{f'{self.calendar_filter}__lte':end_date})


        # Get all filter parameters from the request
        filters = {field: self.request.GET.get(field.replace('_','-'), None) for field, include in self.columns}
        sort_keys = self.request.GET.get('sortKeys', None)
        sort_directions = self.request.GET.get('sortDirections', None)

        if sort_keys is None and sort_directions is None:
            sort_args = [self.default_sort]
        elif sort_keys is None or sort_directions is None:
            raise Exception('Must have GET vars for both sortKeys and sortDirectons or neither')
        else:
            sort_keys = [k.lower().replace('-','_') for k in sort_keys.split(',')]
            sort_directions = ['-' if d == 'descending' else '' for d in sort_directions.split()]
            sort_args = [f'{d}{k}' for k, d in zip(sort_keys, sort_directions)]


        # Apply filters to queryset
        for field, value in filters.items():
            if value:
                queryset = queryset.filter(**{f'{field}__icontains': value})

        return queryset.order_by(*sort_args)

    def build_headers(self):
        """
        Constructs the table header structure.

        Returns a zip object containing:
        - Human readable name (Capitalized, underscores removed)
        - CSS-friendly ID (lower-case-hyphenated)
        - Boolean indicating if a filter input should be rendered
        - Current filter value (to repopulate the input box on reload)
        """
        filter_values = [self.request.GET.get(field.replace('_','-'), None) for field, include in self.columns]
        column_headers_human = [
            ' '.join([w.capitalize() for w in ch.split('_')]) for ch, _ in self.columns
        ]
        include_filter = [i for _, i in self.columns]

        column_headers = [
            ch.lower().replace('_','-') for ch, _ in self.columns
        ]
        return zip(column_headers_human, column_headers, include_filter, filter_values)

    def build_rows(self, context):
        """
        Extracts data from the queryset to pass to the template.

        **CRITICAL LIMITATION:**
        This currently uses `o.__dict__[k]`. 
        This is fast but **dangerous**. It only works for raw database fields.
        It will **crash** if your column is:
        - A `@property` on the model.
        - A `ForeignKey` traversal (e.g., 'user__username').
        - A ManyToMany field.
        
        *Developer Note:* You should almost certainly override this method in your subclass.

        :param context: The Django context to work on
        """
        return [{k: o.__dict__[k] for k, _ in self.columns}for o in context['object_list']]

    def get_context_data(self, **kwargs):
        """
        Bundles all data required for rendering the template.

        Includes:
        - The calculated headers and rows.
        - The current date range (defaults to current month if not provided).
        - URL parameters (to persist state across pagination links).

        :param kwargs: Additional keyword arguments passed to the `HtmlComponent` constructor.
        """
        context = super().get_context_data(**kwargs)
        context['column_headers'] = self.build_headers()
        context['rows'] = self.build_rows(context)

        get_vars = {k: context['view'].request.GET.get(k) for k in context['view'].request.GET}

        if self.calendar_filter is not None:
            now = datetime.now()
            year = now.year
            month = now.month
            start_date = datetime(year=year, month=month, day=1).date()
            if month == 12:
                end_date = datetime(year=year+1, month=1, day=1).date()
            else:
                end_date = datetime(year=year, month=month+1, day=1).date()
            end_date -= timedelta(days=1)

            start_date = self.request.GET.get('start_date', start_date)
            end_date = self.request.GET.get('end_date', end_date)
            context['filter_form'] = TimeRangeForm(
                start_date=start_date,
                end_date=end_date,
            )
            get_vars['start_date'] = start_date
            get_vars['end_date'] = end_date

        context['include_calendar'] = self.calendar_filter is not None
        context['list_table_template'] = self.list_table_template
        context['pagination_template'] = self.pagination_template
        context['title'] = self.title
        context['js_template'] = self.js_template
        context['base_url_path'] = self.base_url_path
        context['get_vars'] = '?' + '&'.join([f'{k}={v}' for k,v in get_vars.items()])
        context['include_subrows'] = True
        # for row in context['rows']:
        #     if 'subrow' in row.keys(): context['include_subrows'] = True
        context['filter_table'] = render(self.request, self.table_template, context).content.decode('utf-8')
        return context


    def render_to_response(self, context, **response_kwargs):
        """
        Handles the "Smart" part of the table update.

        If the request is a standard browser load, it returns the full page.
        If the request is an AJAX call (`X-Requested-With: XMLHttpRequest`), 
        it returns a JSON object containing **only** the HTML strings for the 
        table rows and the pagination controls.
        
        This allows the JavaScript frontend to swap out the table body without 
        refreshing the headers or the rest of the page.

        :param context: The Django context to work in.
        :param response_kwargs: Additional keyword arguments passed to the `HtmlComponent` constructor.

        """
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'html': render(self.request, self.list_table_template, context).content.decode('utf-8'),
                'pagination': render(self.request, self.pagination_template, context).content.decode('utf-8'),
            })
        return super().render_to_response(context, **response_kwargs)