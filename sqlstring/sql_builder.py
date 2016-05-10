# -*- coding: utf-8 -*-

import six
import sqlize  # sql query builder
import sqlparse
from collections_extended import setlist





class StringBuilder(object):
    def __init__(self):
        pass

    def _append_param_item(self, key, param_item):
        try:
            if isinstance(param_item, list):
                for value in param_item:
                    self.param_list_dict[key].append(value)
            else:
                self.param_list_dict[key].append(param_item)
        except:
            pass

    def _get_result_value(self, value_set_list, default_value = None):
        value_list = list(value_set_list)
        value_list.sort()
        result_value = (default_value, value_list)[len(value_list) > 0]

        return (result_value)

    def _init_param_list_dict(self, item_list):
        self.param_list_dict = {}
        for item in item_list:
            self.param_list_dict[item] = setlist()    


class SqlizeSelect(sqlize.Select):
    """ SqlizeSelect is a helper class for internal use. """

    def __init__(self, limit = None, offset = None):
        super(self.__class__, self).__init__(limit = limit, offset = offset)

    def _where_and_list(self, param_list):
        for item in param_list:
            self.where.and_(item)

    def _where_or_list(self, param_list):
        for item in param_list:
            self.where.or_(item)

    def _get_query_string(self, distinct = True, format_sql = False):
        query_string = sqlparse.format(str(self), reindent = format_sql)

        if False == format_sql:
            query_string = ' '.join(query_string.split())

        if True == distinct:
            query_string = query_string.replace('SELECT ', 'SELECT DISTINCT ')

        return (query_string)

    def _get_column_list(self, column_name, order):
        result_list = column_name
        if isinstance(column_name, six.string_types):
            result_list = column_name.split(',')

        if 'DESC' == order.upper():
            result_list = ['-' + item for item in result_list]

        return (result_list)


class SelectBuilder(StringBuilder):
    """ Creates SQL select query string """

    def __init__(self, limit = None, offset = None, distinct = False):
        super(self.__class__, self).__init__()
        self._sqlize_select = SqlizeSelect(limit = limit, offset = offset)
        self.distinct(distinct)
        item_list = ['table', 'column', 'where', 'where_and', 'where_or', 'group_by', 'order_by']
        self._init_param_list_dict(item_list)


    def from_table(self, table_name):
        """
        Adding one or more `table` to `SQL` SELECT query string.

        :Example:
        >>> from sqlstring.sql_builder import SelectBuilder
        >>> builder = SelectBuilder()
        >>> builder.from_table('address').get_query_string()
        SELECT * FROM address;

        :param table_name: `list` or `str`
        :return: an object of type `SelectBuilder`
        """

        self._append_param_item('table', table_name)
        return (self)

    def column(self, column_name):
        """
        Adding one or more `column` to `SELECT` query string.

        :Example:
        >>> from sqlstring.sql_builder import SelectBuilder
        >>> builder = SelectBuilder()
        >>> builder.from_table('address').column(['city', 'state_code']).get_query_string()
        SELECT city, state_code FROM address;

        :param column_name: `list` or `str`
        :return: an object of type `SelectBuilder`
        """
        self._append_param_item('column', column_name)
        return (self)

    def where(self, column_name, op, value, where_type = 'where'):
        """
        Adding a `where` clause to `SELECT` query string.

        :Example:
        >>> from sqlstring.sql_builder import SelectBuilder
        >>> builder = SelectBuilder()
        >>> builder.from_table('address').where('state_code', '=', " 'CA' ")
        >>> builder.where('city', '=', " 'Oakland' ", 'AND')
        >>> builder.get_query_string()
        SELECT * FROM address WHERE state_code = 'CA' AND city = 'Oakland';

        :param column_name: `list` or `str`
        :param op: `str`
        :param value:
        :param where_type: `str`, values `'AND'`, `'OR'`, default `'where'`
        :return: an object of type `SelectBuilder`
        """
        where_type = where_type.strip()
        where_item = where_type
        if 'where' != where_type.lower():
            where_item = ('where_and', 'where_or')['OR' == where_type.upper()]

        where_string = " {0} {1} {2} ".format(column_name, op, value)
        self._append_param_item(where_item, where_string)

        return (self)

    def group_by(self, column_name):
        """
        Adding a `GROUP BY` clause to `SELECT` query string.

        :Example:
        >>> from sqlstring.sql_builder import SelectBuilder
        >>> builder = SelectBuilder()
        >>> builder.from_table('address').group_by(['state_code', 'city']).get_query_string()
        SELECT * FROM address GROUP BY city, state_code;

        :param column_name: `list` or `str`
        :return: an object of type `SelectBuilder`
        """
        self._append_param_item('group_by', column_name)
        return (self)

    def order_by(self, column_name, order = 'ASC'):
        """
        Adding a `ORDER BY` clause to `SELECT` query string.

        :Example:
        >>> from sqlstring.sql_builder import SelectBuilder
        >>> builder = SelectBuilder()
        >>> builder.from_table('address').order_by(['state_code', 'city'], 'DESC').get_query_string()
        SELECT * FROM address ORDER BY city DESC, state_code DESC;

        :param column_name: `list` or `str`
        :param order: `str`, values `'DESC'`, default `'ASC'`
        :return: an object of type `SelectBuilder`
        """
        column_list = self._sqlize_select._get_column_list(column_name, order)
        self._append_param_item('order_by', column_list)

        return (self)

    def limit(self, value):
        """
        Adding a `LIMIT` clause to `SELECT` query string.

        :Example:
        >>> from sqlstring.sql_builder import SelectBuilder
        >>> builder = SelectBuilder()
        >>> builder.from_table('address').limit(5).get_query_string()
        SELECT * FROM address LIMIT 5;

        :param value: `int`
        :return: an object of type `SelectBuilder`
        """
        self._sqlize_select.limit = int(value)
        return (self)

    def offset(self, value):
        """
        Adding a `OFFSET` clause to `SELECT` query string.

        :Example:
        >>> from sqlstring.sql_builder import SelectBuilder
        >>> builder = SelectBuilder()
        >>> builder.from_table('address').limit(100).offset(200).get_query_string()
        SELECT * FROM address LIMIT 100 OFFSET 200;

        :param value: `int`
        :return: an object of type `SelectBuilder`
        """
        self._sqlize_select.offset = int(value)
        return (self)

    def distinct(self, value = True):
        """
        Adding a `DISTINCT` keyword to `SELECT` query string.

        :Example:
        >>> from sqlstring.sql_builder import SelectBuilder
        >>> builder = SelectBuilder()
        >>> builder.from_table('address').distinct().get_query_string()
        SELECT DISTINCT * FROM address;

        :param value: `bool`
        :return: an object of type `SelectBuilder`
        """
        self.distinct_value = bool(value)
        return (self)

    def get_query_string(self, format_sql = False):
        """
        Returning a `SELECT` query string.

        :Example:
        >>> from sqlstring.sql_builder import SelectBuilder
        >>> builder = SelectBuilder()
        >>> builder.from_table('address').get_query_string()
        SELECT * FROM address;

        :param format_sql: `bool`, default value `False`
        :return: SQL query string of type `str`
        """

        #
        self._sqlize_select.sets = self._get_result_value(self.param_list_dict['table'])
        self._sqlize_select.what = self._get_result_value(self.param_list_dict['column'], ['*'])
        self._sqlize_select.where = self._get_result_value(self.param_list_dict['where'])
        self._sqlize_select._where_and_list(list(self.param_list_dict['where_and']))
        self._sqlize_select._where_or_list(list(self.param_list_dict['where_or']))
        self._sqlize_select.group = self._get_result_value(self.param_list_dict['group_by'])
        self._sqlize_select.order = self._get_result_value(self.param_list_dict['order_by'])

        query_string = self._sqlize_select._get_query_string(distinct = self.distinct_value, format_sql = format_sql)

        return (query_string)


class InsertBuilder(StringBuilder):
    """ Creates SQL `INSERT` query string """

    def __init__(self, table_name = None):
        super(self.__class__, self).__init__()
        item_list = ['column']
        self._init_param_list_dict(item_list)
        if bool(table_name):
            self.into_table(table_name)
            

    def _get_query_string(self, insert_suffix = None, format_sql = False):
        query_string = sqlparse.format(str(self), reindent = format_sql)

        if False == format_sql:
            query_string = ' '.join(query_string.split())

        if None != insert_suffix:
            insert_string = "INSERT {0} ".format(insert_suffix)
            query_string = query_string.replace('INSERT ', insert_string)

        return (query_string)


    def into_table(self, table_name):
        """
        Adding one or more `table` to `INSERT` query string.

        :Example:
        >>> from sqlstring.sql_builder import InsertBuilder
        >>> builder = InsertBuilder()
        >>> builder.from_table('address').column(['city', 'state_code']).get_query_string()
        INSERT INTO address (city, state_code) VALUES (:city, :state_code);

        :param table_name: `str`
        :return: an object of type `SelectBuilder`
        """

        self.table_name = table_name
        return (self)


    def column(self, column_name):
        """
        Adding one or more `column` to `INSERT` query string.

        :Example:
        >>> from sqlstring.sql_builder import InsertBuilder
        >>> builder = InsertBuilder()
        >>> builder.from_table('address').column(['city', 'state_code']).get_query_string()
        INSERT INTO address (city, state_code) VALUES (:city, :state_code);

        :param column_name: `list` or `str`
        :return: an object of type `SelectBuilder`
        """
        self._append_param_item('column', column_name)
        return (self)


    def get_query_string(self, insert_suffix = None, format_sql = False):
        """
        Returning a `INSERT` query string.

        :Example:
        >>> from sqlstring.sql_builder import InsertBuilder
        >>> builder = InsertBuilder()
        >>> builder.from_table('address').column(['city', 'state_code']).get_query_string()
        INSERT INTO address (city, state_code) VALUES (:city, :state_code);

        :param format_sql: `bool`, default value `False`
        :return: SQL query string of type `str`
        """
        sqlize_insert = sqlize.Insert(self.table_name)
        sqlize_insert.cols = self._get_result_value(self.param_list_dict['column'])

        query_string = self._get_query_string(insert_suffix = insert_suffix, format_sql = format_sql)

        return (query_string)