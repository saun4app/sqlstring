
Introduction
=========================================
.. toctree::
   :hidden:

`sqlstring` is a Python library for creating SQL query strings.  `sqlstring` has four query string building classes: `SelectBuilder`, `InsertBuilder`
`UpdateBuilder`, and `DeleteBuilder`.

Here is an an example of crating `select` query string using `SelectBuilder`:

::

    from sqlstring.sql_builder import SelectBuilder

    builder = SelectBuilder()
    builder.from_table('address').where('state_code', '=', " 'CA' ")
    builder.where('city', '=', " 'Oakland' ", 'AND')
    query_string = builder.get_query_string()
    # SELECT * FROM address WHERE state_code = 'CA' AND city = 'Oakland';



Installation
--------

Install ``sqlstring`` from the `Python Package Index <https://pypi.python.org/pypi/sqlstring/>`_ using ``pip``

.. code-block:: bash

   $ pip install sqlstring


from `github <https://github.com/saun4app/sqlstring>`_ using ``pip``

.. code-block:: bash

   $ pip install git+https://github.com/saun4app/sqlstring.git


Credits
--------

`sqlstring <https://github.com/saun4app/sqlstring>`_ uses

* `sqlize <https://pypi.python.org/pypi/sqlize/>`_ to creat the query strings.
* `generator-python-lib <https://github.com/hbetts/generator-python-lib/>`_ to scaffold the project.
* `jupyter <https://pypi.python.org/pypi/jupyter/>`_, `nbsphinx <https://pypi.python.org/pypi/nbsphinx/>`_, `sphinx <https://pypi.python.org/pypi/sphinx/>`_, `sphinx-rtd-theme <https://pypi.python.org/pypi/sphinx-rtd-theme/>`_ for documentation.


.. toctree::
   :maxdepth: 2
