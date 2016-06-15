from unittest import TestCase


from sqlstring.sql_builder import DeleteBuilder

class TestDeleteBuilder(TestCase):

    def setUp(self):
        pass

    def test_from_table(self):
        builder = DeleteBuilder()
        builder.from_table('address').where('state_code', '=', " 'CA' ")
        builder.where('city', '=', " 'Oakland' ", 'AND')
        r = builder.get_query_string()

        self.assertEqual(len(r), 65)

    def test_get_query_string(self):
        pass

