from unittest import TestCase

from sqlstring.sql_builder import InsertBuilder

class TestInsertBuilder(TestCase):

    def setUp(self):
        pass

    def test_into_table(self):
        builder = InsertBuilder()
        builder.into_table('address').column(['city', 'state_code'])
        r = builder.get_query_string()

        self.assertEqual(len(r), 67)

    def test_column(self):
        pass

    def test_get_query_string(self):
        pass
