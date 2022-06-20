from ast import Add
import unittest
from utils.flask_utils import add_to_where_clause, create_route

class TestWhereClause(unittest.TestCase):
    
    def test_add_to_where_clause(self):
        
        execution_statement = ["SELECT * FROM table WHERE x = %(y)s"]
        execution_arguments = {"y": "y"}
        new_argument_name = "date"
        value = "2022-1-1"
    
        add_to_where_clause(
            execution_statement,
            execution_arguments,
            new_argument_name,
            value
        )
        
        self.assertEqual(execution_statement, ["SELECT * FROM table WHERE x = %(y)s", "AND date = %(date)s"])
        self.assertEqual(execution_arguments, {"y": "y", "date": "2022-1-1"})

            
        
        
