Custom Python Reports
======================

This page demonstrates custom Python-generated content in the documentation.

System Information
------------------

.. custom-report:: system_info

Component Table
---------------

.. custom-report:: component_table

Adding Your Own Reports
-----------------------

To add custom reports:

1. Edit ``docs/_ext/custom_reports.py``
2. Add a new function that returns HTML (e.g., ``generate_my_report()``)
3. Register it in ``CustomReportDirective.run()`` method
4. Use it in any ``.rst`` file with: ``.. custom-report:: my_report``

Your custom functions have full access to Python - you can:

* Query APIs
* Read files from the repository
* Generate charts with matplotlib/plotly
* Create tables from data
* Run any Python code during the doc build

The function just needs to return an HTML string.
