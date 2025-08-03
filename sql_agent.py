import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text, inspect
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import json
import re

class SQLAgent:
    def __init__(self, database_path, api_key):
        """
        Initialize SQL Agent with database path and Google Gemini API key
        
        Args:
            database_path (str): Path to SQLite database
            api_key (str): Google Gemini API key
        """
        self.database_path = database_path
        self.engine = create_engine(f'sqlite:///{database_path}')
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            google_api_key=api_key
        )
        
        # Get database schema
        self.schema = self._get_database_schema()
        
    def _get_database_schema(self):
        """Extract database schema information"""
        inspector = inspect(self.engine)
        schema_info = {}
        
        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            schema_info[table_name] = {
                'columns': [col['name'] for col in columns],
                'types': {col['name']: col['type'] for col in columns}
            }
            
            # Get sample data for better understanding
            try:
                sample_query = f"SELECT * FROM {table_name} LIMIT 5"
                sample_data = pd.read_sql_query(sample_query, self.engine)
                schema_info[table_name]['sample_data'] = sample_data.to_dict('records')
            except Exception as e:
                print(f"Warning: Could not get sample data for table {table_name}: {e}")
                schema_info[table_name]['sample_data'] = []
        
        return schema_info
    
    def _create_schema_prompt(self):
        """Create a detailed schema description for the LLM"""
        schema_text = "Database Schema:\n\n"
        
        for table_name, table_info in self.schema.items():
            schema_text += f"Table: {table_name}\n"
            schema_text += "Columns:\n"
            
            for col_name, col_type in table_info['types'].items():
                schema_text += f"  - {col_name} ({col_type})\n"
            
            # Add sample data if available
            if table_info['sample_data']:
                schema_text += "Sample data:\n"
                for i, row in enumerate(table_info['sample_data'][:3]):  # Show first 3 rows
                    schema_text += f"  Row {i+1}: {row}\n"
            
            schema_text += "\n"
        
        # Add relationship hints if multiple tables
        if len(self.schema) > 1:
            schema_text += "RELATIONSHIP HINTS:\n"
            schema_text += "- When joining tables, look for common column names (like 'id', 'customer_id', etc.)\n"
            schema_text += "- Use appropriate JOIN types (INNER, LEFT, RIGHT, FULL) based on the question\n"
            schema_text += "- Consider using table aliases for clarity in complex queries\n"
            schema_text += "- When comparing data across tables, use UNION or JOIN as appropriate\n\n"
        
        return schema_text
    
    def generate_sql(self, question):
        """
        Generate SQL query from natural language question
        
        Args:
            question (str): Natural language question
            
        Returns:
            str: Generated SQL query
        """
        schema_prompt = self._create_schema_prompt()
        
        # Create the prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert SQL developer. Your task is to convert natural language questions into SQL queries.

CRITICAL RULES:
1. Generate ONLY the SQL query - no explanations, no markdown, no extra text
2. Start the response directly with SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, or WITH
3. Use SQLite syntax
4. Always use proper table and column names from the schema
5. Use LIMIT when appropriate for large datasets
6. Use proper SQL functions (COUNT, SUM, AVG, etc.)
7. Handle date/time operations appropriately
8. Use proper JOIN syntax when needed
9. Always end queries with semicolon
10. Do not include any text before or after the SQL query
11. For multiple tables, use appropriate JOINs based on common columns
12. When comparing data across tables, use UNION or JOIN as appropriate
13. Use table aliases (e.g., 's' for sales, 'e' for employees) for clarity in complex queries

{schema}

The user will ask a question about the data. Generate ONLY the SQL query starting with a SQL keyword."""),
            ("human", "Question: {question}\n\nGenerate SQL query:")
        ])
        
        # Create the chain
        chain = prompt_template | self.llm
        
        # Generate SQL
        response = chain.invoke({
            "schema": schema_prompt,
            "question": question
        })
        
        # Extract SQL from response
        sql_query = response.content.strip()
        
        # Clean up the SQL query
        sql_query = self._clean_sql_query(sql_query)
        
        return sql_query
    
    def _clean_sql_query(self, sql_query):
        """Clean and validate SQL query"""
        # Remove markdown code blocks if present
        sql_query = re.sub(r'```sql\s*', '', sql_query)
        sql_query = re.sub(r'```\s*', '', sql_query)
        
        # Remove leading/trailing whitespace
        sql_query = sql_query.strip()
        
        # Find the first occurrence of SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER
        # This handles cases where the LLM adds extra text before the SQL
        sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER', 'WITH']
        for keyword in sql_keywords:
            if keyword in sql_query.upper():
                start_idx = sql_query.upper().find(keyword)
                sql_query = sql_query[start_idx:]
                break
        
        # Ensure it ends with semicolon
        if not sql_query.endswith(';'):
            sql_query += ';'
        
        return sql_query
    
    def execute_query(self, sql_query):
        """
        Execute SQL query and return results
        
        Args:
            sql_query (str): SQL query to execute
            
        Returns:
            pandas.DataFrame: Query results
        """
        try:
            # Additional validation before execution
            if not sql_query.strip():
                raise Exception("Empty SQL query")
            
            # Check if query starts with a valid SQL keyword
            sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER', 'WITH']
            query_upper = sql_query.strip().upper()
            if not any(query_upper.startswith(keyword) for keyword in sql_keywords):
                raise Exception(f"Invalid SQL query format. Query must start with a SQL keyword. Got: {sql_query[:50]}...")
            
            # Execute query
            results = pd.read_sql_query(sql_query, self.engine)
            return results
        except Exception as e:
            raise Exception(f"Error executing SQL query: {str(e)}")
    
    def get_table_info(self, table_name=None):
        """
        Get information about tables in the database
        
        Args:
            table_name (str, optional): Specific table name. If None, returns all tables.
            
        Returns:
            dict: Table information
        """
        if table_name:
            return self.schema.get(table_name, {})
        return self.schema
    
    def get_sample_queries(self):
        """Get sample queries based on the database schema"""
        sample_queries = []
        
        for table_name, table_info in self.schema.items():
            columns = table_info['columns']
            
            # Basic queries
            sample_queries.extend([
                f"Show me the first 10 rows from {table_name}",
                f"Count the total number of records in {table_name}",
                f"Show me all unique values in the first column of {table_name}"
            ])
            
            # Numeric column queries
            numeric_cols = [col for col, dtype in table_info['types'].items() 
                          if 'int' in str(dtype).lower() or 'float' in str(dtype).lower()]
            
            if numeric_cols:
                sample_queries.extend([
                    f"Calculate the average of {numeric_cols[0]} in {table_name}",
                    f"Find the maximum value of {numeric_cols[0]} in {table_name}",
                    f"Show me the top 5 records by {numeric_cols[0]} in {table_name}"
                ])
        
        return sample_queries[:10]  # Return first 10 samples
    
    def validate_query(self, sql_query):
        """
        Validate SQL query without executing it
        
        Args:
            sql_query (str): SQL query to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Try to compile the query
            with self.engine.connect() as conn:
                conn.execute(text(sql_query))
            return True
        except Exception:
            return False
    
    def explain_query(self, sql_query):
        """
        Explain what a SQL query does
        
        Args:
            sql_query (str): SQL query to explain
            
        Returns:
            str: Explanation of the query
        """
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are an expert SQL developer. Explain what the following SQL query does in simple terms:"),
            ("human", "SQL Query: {sql_query}\n\nExplain what this query does:")
        ])
        
        chain = prompt_template | self.llm
        
        response = chain.invoke({"sql_query": sql_query})
        return response.content.strip() 