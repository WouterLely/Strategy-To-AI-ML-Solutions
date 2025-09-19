"""
Database handler for structured data queries using LlamaIndex
"""
import sqlite3
import os
from typing import List, Dict, Any, Optional
from llama_index.core import SQLDatabase, VectorStoreIndex
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.objects import SQLTableNodeMapping, ObjectIndex, SQLTableSchema
from llama_index.core import Settings
from sqlalchemy import create_engine, MetaData, Table


class DatabaseHandler:
    """Handles structured data queries using SQL and LlamaIndex"""
    
    def __init__(self, db_path: str = "data/database/company.db"):
        self.db_path = db_path
        self.engine = None
        self.sql_database = None
        self.query_engine = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize the database connection and LlamaIndex SQL components"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database not found at {self.db_path}")
        
        # Create SQLAlchemy engine
        self.engine = create_engine(f"sqlite:///{self.db_path}")
        
        # Create LlamaIndex SQL database
        self.sql_database = SQLDatabase(self.engine, include_tables=[
            "employees", "departments", "customers", "products", "orders", "order_details"
        ])
        
        # Create query engine
        self.query_engine = NLSQLTableQueryEngine(
            sql_database=self.sql_database,
            tables=["employees", "departments", "customers", "products", "orders", "order_details"]
        )
    
    def query(self, question: str) -> str:
        """Query the database using natural language"""
        try:
            response = self.query_engine.query(question)
            return str(response)
        except Exception as e:
            return f"Error querying database: {str(e)}"
    
    def get_table_info(self) -> Dict[str, Any]:
        """Get information about available tables and their schemas"""
        tables_info = {}
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get all table names
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                for (table_name,) in tables:
                    # Get column information for each table
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = cursor.fetchall()
                    
                    tables_info[table_name] = {
                        "columns": [
                            {
                                "name": col[1],
                                "type": col[2],
                                "not_null": bool(col[3]),
                                "primary_key": bool(col[5])
                            }
                            for col in columns
                        ]
                    }
                    
                    # Get row count
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                    count = cursor.fetchone()[0]
                    tables_info[table_name]["row_count"] = count
        
        except Exception as e:
            tables_info["error"] = str(e)
        
        return tables_info
    
    def execute_sql(self, sql_query: str) -> List[Dict[str, Any]]:
        """Execute a raw SQL query and return results"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row  # Enable column access by name
                cursor = conn.cursor()
                cursor.execute(sql_query)
                
                # Convert to list of dictionaries
                results = [dict(row) for row in cursor.fetchall()]
                return results
        
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_sample_queries(self) -> List[str]:
        """Return sample queries that users can try"""
        return [
            "How many employees work in each department?",
            "What is the average salary by department?",
            "Which sales representatives have the highest sales this year?",
            "Show me all orders from the last 6 months",
            "What are the top 5 best-selling products?",
            "Which customers have placed the most orders?",
            "What is the total revenue by month?",
            "Show me employees hired in the last year",
            "Which departments have the highest budgets?",
            "What is the average order value by customer?"
        ]
