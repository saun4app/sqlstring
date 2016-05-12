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

    def _get_result_value(self, value_set_list, default_value = None, sort_list = True):
        value_list = list(value_set_list)
        if True == sort_list:
            value_list.sort()
        result_value = (default_value, value_list)[len(value_list) > 0]

        return (result_value)

    def _init_param_list_dict(self, item_list):
        self.param_list_dict = {}
        for item in item_list:
            self.param_list_dict[item] = setlist()

    def _where(self, column_name, op, value, where_type = 'where'):
        where_type = where_type.strip()
        where_item = where_type
        if 'where' != where_type.lower():
            where_item = ('where_and', 'where_or')['OR' == where_type.upper()]

        where_string = " {0} {1} {2} ".format(column_name, op, value)
        self._append_param_item(where_item, where_string)

        return (self)

    def _where_and_list(self, sqlize_object, param_list):
        for item in param_list:
            sqlize_object.where.and_(item)

    def _where_or_list(self, sqlize_object, param_list):
        for item in param_list:
            sqlize_object.where.or_(item)

    def where(self, column_name, op, value, where_type = 'where'):
        """
        Adding a `where` clause to query string.

        :param column_name: `list` or `str`
        :param op: `str`
        :param value:
        :param where_type: `str`, values `'AND'`, `'OR'`, default `'where'`
        :return: `self` object
        """
        self._where(column_name, op, value, where_type)
        return (self)


class SelectBuilder(StringBuilder):
    """ Creates SQL select query string """

    def __init__(self, limit = None, offset = None, distinct = False):
        # super(self.__class__, self).__init__()
        self._sqlize_select = sqlize.Select(limit = limit, offset = offset)
        self.distinct(distinct)
        self.join_table_dict = {}

        item_list = ['table', 'column', 'where', 'where_and', 'where_or', 'group_by', 'order_by']
        self._init_param_list_dict(item_list)

    def _get_query_string(self, distinct = True, format_sql = False):
        query_string = sqlparse.format(str(self._sqlize_select), reindent = format_sql)

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

    def from_table(self, table_name):
        """
        Adding one or more `table` to `SQL` SELECT query string.

        :param table_name: `list` or `str`
        :return: `self` object
        """
        self._append_param_item('table', table_name)
        return (self)

    def column(self, column_name):
        """
        Adding one or more `column` to `SELECT` query string.

        :param column_name: `list` or `str`
        :return: `self` object
        """
        self._append_param_item('column', column_name)
        return (self)

    def group_by(self, column_name):
        """
        Adding a `GROUP BY` clause to `SELECT` query string.

        :param column_name: `list` or `str`
        :return: `self` object
        """
        self._append_param_item('group_by', column_name)
        return (self)

    def order_by(self, column_name, order = 'ASC'):
        """
        Adding a `ORDER BY` clause to `SELECT` query string.

        :param column_name: `list` or `str`
        :param order: `str`, values `'DESC'`, default `'ASC'`
        :return: `self` object
        """
        column_list = self._get_column_list(column_name, order)
        self._append_param_item('order_by', column_list)

        return (self)

    def limit(self, value):
        """
        Adding a `LIMIT` clause to `SELECT` query string.

        :param value: `int`
        :return: `self` object
        """
        self._sqlize_select.limit = int(value)
        return (self)

    def offset(self, value):
        """
        Adding a `OFFSET` clause to `SELECT` query string.

        :param value: `int`
        :return: `self` object
        """
        self._sqlize_select.offset = int(value)
        return (self)

    def distinct(self, value = True):
        """
        Adding a `DISTINCT` keyword to `SELECT` query string.

        :param value: `bool`
        :return: `self` object
        """
        self.distinct_value = bool(value)
        return (self)

    def join_table(self, join_table_name, join_type = sqlize.INNER):
        """
        Adding a `DISTINCT` keyword to `SELECT` query string.

        :param join_table_name: `str`
        :param join_type: `str`, default `sqlize.INNER`
        :return: `self` object
        """
        self.join_table_dict = {'table_name': join_table_name, 'join_type': join_type}
        return (self)

    def get_query_string(self, format_sql = False):
        """
        Returning a `SELECT` query string.

        :param format_sql: `bool`, default value `False`
        :return: SQL query string of type `str`
        """
        self._sqlize_select.sets = self._get_result_value(self.param_list_dict['table'])
        self._sqlize_select.what = self._get_result_value(self.param_list_dict['column'], default_value = ['*'])
        self._sqlize_select.where = self._get_result_value(self.param_list_dict['where'])
        self._where_and_list(self._sqlize_select, list(self.param_list_dict['where_and']))
        self._where_or_list(self._sqlize_select, list(self.param_list_dict['where_or']))
        self._sqlize_select.group = self._get_result_value(self.param_list_dict['group_by'], sort_list = False)
        self._sqlize_select.order = self._get_result_value(self.param_list_dict['order_by'], sort_list = False)

        if bool(self.join_table_dict):
            self._sqlize_select.sets.join(self.join_table_dict['table_name'], self.join_table_dict['join_type'])

        query_string = self._get_query_string(distinct = self.distinct_value, format_sql = format_sql)

        return (query_string)


class InsertBuilder(StringBuilder):
    """
    Creates SQL `INSERT` query string.  InsertBuilder enables the use of some SQL dialect,
    e.g., `IGNORE` for `MySQL`, and `OR REPLACE` for `Sqlite`.
    """

    def __init__(self, table_name = None):
        # super(self.__class__, self).__init__()
        item_list = ['column']
        self._init_param_list_dict(item_list)
        if bool(table_name):
            self.into_table(table_name)

    def _get_query_string(self, sqlize_insert, insert_suffix = None, format_sql = False):
        query_string = sqlparse.format(str(sqlize_insert), reindent = format_sql)

        if False == format_sql:
            query_string = ' '.join(query_string.split())

        if None != insert_suffix:
            insert_string = "INSERT {0} ".format(insert_suffix)
            query_string = query_string.replace('INSERT ', insert_string)

        return (query_string)

    def into_table(self, table_name):
        """
        Adding one or more `table` to `INSERT` query string.

        :param table_name: `str`
        :return: `self` object
        """
        self.table_name = table_name
        return (self)

    def column(self, column_name):
        """
        Adding one or more `column` to `INSERT` query string.

        :param column_name: `list` or `str`
        :return: `self` object
        """
        self._append_param_item('column', column_name)
        return (self)

    def get_query_string(self, insert_suffix = None, format_sql = False):
        """
        Returning a `INSERT` query string.

        :param insert_suffix: `str`, `IGNORE`, `OR REPLACE`, default None
        :param format_sql: `bool`, default value `False`
        :return: SQL query string of type `str`
        """
        column_list = self._get_result_value(self.param_list_dict['column'])
        sqlize_insert = sqlize.Insert(self.table_name, cols = column_list)

        query_string = self._get_query_string(sqlize_insert, insert_suffix = insert_suffix, format_sql = format_sql)

        return (query_string)


class UpdateBuilder(StringBuilder):
    """ Creates SQL `UPDATE` query string. """

    def __init__(self, table_name = None):
        # super(self.__class__, self).__init__()
        self.set_value_dict = {}

        item_list = ['where', 'where_and', 'where_or']
        self._init_param_list_dict(item_list)
        if bool(table_name):
            self.update_table(table_name)

    def _get_query_string(self, sqlize_update, format_sql = False):
        query_string = sqlparse.format(str(sqlize_update), reindent = format_sql)

        if False == format_sql:
            query_string = ' '.join(query_string.split())

        return (query_string)

    def update_table(self, table_name):
        """
        Adding one or more `table` to `UPDATE` query string.

        :param table_name: `str`
        :return: `self` object
        """
        self.table_name = table_name
        return (self)

    def set(self, column_name, value):
        """
        Adding a `SET` clause to `UPDATE` query string.

        :param column_name: `list` or `str`
        :param value:
        :param where_type: `str`, values `'AND'`, `'OR'`, default `'where'`
        :return: `self` object
        """
        self.set_value_dict[column_name] = value
        return (self)

    def get_query_string(self, format_sql = False):
        """
        Returning a `UPDATE` query string.

        :param format_sql: `bool`, default value `False`
        :return: SQL query string of type `str`
        """
        sqlize_update = sqlize.Update(self.table_name, **self.set_value_dict)
        sqlize_update.where = self._get_result_value(self.param_list_dict['where'])
        self._where_and_list(sqlize_update, list(self.param_list_dict['where_and']))
        self._where_or_list(sqlize_update, list(self.param_list_dict['where_or']))

        query_string = self._get_query_string(sqlize_update, format_sql = format_sql)

        return (query_string)


class DeleteBuilder(StringBuilder):
    """ Creates SQL `DELETE` query string. """

    def __init__(self, table_name = None):
        # super(self.__class__, self).__init__()
        item_list = ['where', 'where_and', 'where_or']
        # item_list = ['where']
        self._init_param_list_dict(item_list)
        if bool(table_name):
            self.from_table(table_name)

    def _get_query_string(self, sqlize_delete, format_sql = False):
        query_string = sqlparse.format(str(sqlize_delete), reindent = format_sql)

        if False == format_sql:
            query_string = ' '.join(query_string.split())

        return (query_string)

    def from_table(self, table_name):
        """
        Adding one or more `table` to `DELETE` query string.

        :param table_name: `str`
        :return: `self` object
        """
        self.table_name = table_name
        return (self)

    def get_query_string(self, format_sql = False):
        """
        Returning a `INSERT` query string.

        :param format_sql: `bool`, default value `False`
        :return: SQL query string of type `str`
        """
        sqlize_delete = sqlize.Delete(self.table_name)
        sqlize_delete.where = self._get_result_value(self.param_list_dict['where'])
        self._where_and_list(sqlize_delete, list(self.param_list_dict['where_and']))
        self._where_or_list(sqlize_delete, list(self.param_list_dict['where_or']))

        query_string = self._get_query_string(sqlize_delete, format_sql = format_sql)

        return (query_string)
