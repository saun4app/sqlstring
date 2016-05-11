from unittest import TestCase

from sqlstring.sql_builder import UpdateBuilder


class TestUpdateBuilder(TestCase):
    def setUp(self):
        pass

    def test_update_table(self):
        builder = UpdateBuilder()
        builder.update_table('address').set('state_name', " 'California' ")
        r = builder.get_query_string()

        self.assertEqual(len(r), 46)

    def test_set(self):
        pass

    def test_get_query_string(self):
        pass
