import streamlit as st
import pandas as pd
import sqlite3
import os
from sqlalchemy import create_engine, text
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
from sql_agent import SQLAgent

# Page configuration
st.set_page_config(
    page_title="SQL Agent - Excel to SQL",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .question-section {
        background-color: #e8f4fd;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .result-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .sql-code {
        background-color: #2d3748;
        color: #e2e8f0;
        padding: 1rem;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'sql_agent' not in st.session_state:
    st.session_state.sql_agent = None
if 'database_path' not in st.session_state:
    st.session_state.database_path = None
if 'table_name' not in st.session_state:
    st.session_state.table_name = None

def create_database_from_excel(df, table_name):
    """Create SQLite database from Excel data"""
    # Create a unique database file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    db_path = f"temp_database_{timestamp}.db"
    
    # Create SQLite engine
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Write DataFrame to SQL
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    
    return db_path, engine

def display_data_preview(df):
    """Display data preview with statistics"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
    
    with col2:
        st.subheader("📊 Data Statistics")
        st.write(f"**Rows:** {len(df)}")
        st.write(f"**Columns:** {len(df.columns)}")
        st.write(f"**Memory Usage:** {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
        
        # Column types
        st.write("**Column Types:**")
        for col, dtype in df.dtypes.items():
            st.write(f"- {col}: {dtype}")

def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 SQL Agent - Excel to SQL</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input("Google Gemini API Key", type="password", help="Enter your Google Gemini API key", value=st.session_state.get('api_key', ''))
        
        if api_key:
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ Please enter your Google Gemini API key")
        
        st.markdown("---")
        
        # Instructions
        st.header("📖 How to Use")
        st.markdown("""
        1. **Upload Excel File** - Drag and drop your Excel file
        2. **Ask Questions** - Use natural language to query your data
        3. **Get SQL & Results** - View generated SQL and data insights
        """)
        
        st.markdown("---")
        
        # Pre-configured API key
        if st.button("🔑 Use Provided API Key"):
            st.session_state.api_key = "AIzaSyAOahaYB1qof3ZQLdy7Nhv2amJfVjFxRjI"
            st.success("✅ Using provided Gemini API key")
        
        st.markdown("---")
        
        # Example questions
        st.header("💡 Example Questions")
        st.markdown("""
        - "Show me the top 10 sales by region"
        - "What is the average salary by department?"
        - "Find all employees hired in 2023"
        - "Calculate total revenue by month"
        - "Show me the distribution of ages"
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File upload section
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.header("📁 Upload Excel File")
        
        uploaded_file = st.file_uploader(
            "Choose an Excel file",
            type=['xlsx', 'xls'],
            help="Upload your Excel file to start querying"
        )
        
        if uploaded_file is not None:
            try:
                # Read Excel file
                df = pd.read_excel(uploaded_file)
                st.session_state.uploaded_data = df
                
                # Get table name from file
                table_name = uploaded_file.name.split('.')[0].replace(' ', '_').lower()
                st.session_state.table_name = table_name
                
                # Create database
                db_path, engine = create_database_from_excel(df, table_name)
                st.session_state.database_path = db_path
                
                # Initialize SQL Agent
                if api_key:
                    st.session_state.sql_agent = SQLAgent(db_path, api_key)
                
                st.success(f"✅ File uploaded successfully! Table name: `{table_name}`")
                
                # Display data preview
                display_data_preview(df)
                
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Quick stats
        if st.session_state.uploaded_data is not None:
            st.header("📈 Quick Stats")
            df = st.session_state.uploaded_data
            
            # Basic statistics
            st.metric("Total Rows", len(df))
            st.metric("Total Columns", len(df.columns))
            
            # Numeric columns summary
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                st.subheader("Numeric Columns")
                for col in numeric_cols[:3]:  # Show first 3
                    st.metric(f"Avg {col}", f"{df[col].mean():.2f}")
    
    # Question and query section
    if st.session_state.uploaded_data is not None and st.session_state.sql_agent is not None:
        st.markdown('<div class="question-section">', unsafe_allow_html=True)
        st.header("❓ Ask Questions About Your Data")
        
        # Question input
        question = st.text_area(
            "Enter your question:",
            placeholder="e.g., Show me the top 10 sales by region",
            height=100
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🔍 Generate SQL & Execute", type="primary"):
                if question.strip():
                    with st.spinner("🤖 Generating SQL query..."):
                        try:
                            # Generate SQL query
                            sql_query = st.session_state.sql_agent.generate_sql(question)
                            
                            # Execute query
                            results = st.session_state.sql_agent.execute_query(sql_query)
                            
                            # Store results in session state
                            st.session_state.last_sql = sql_query
                            st.session_state.last_results = results
                            
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                            st.error("💡 Tip: Try rephrasing your question or check if the table/column names exist in your data.")
                else:
                    st.warning("Please enter a question")
        
        with col2:
            if st.button("📊 Show Sample Queries"):
                st.session_state.show_samples = True
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display results
        if hasattr(st.session_state, 'last_sql') and hasattr(st.session_state, 'last_results'):
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            st.header("📋 Results")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("🔧 Generated SQL Query")
                st.markdown(f'<div class="sql-code">{st.session_state.last_sql}</div>', unsafe_allow_html=True)
                
                # Copy button
                if st.button("📋 Copy SQL"):
                    st.write("SQL copied to clipboard!")
            
            with col2:
                st.subheader("📊 Query Results")
                if isinstance(st.session_state.last_results, pd.DataFrame):
                    st.dataframe(st.session_state.last_results, use_container_width=True)
                    
                    # Download results
                    csv = st.session_state.last_results.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.write(st.session_state.last_results)
            
            # Visualization
            if isinstance(st.session_state.last_results, pd.DataFrame) and len(st.session_state.last_results) > 0:
                st.subheader("📈 Visualizations")
                
                # Auto-generate charts based on data
                df_results = st.session_state.last_results
                numeric_cols = df_results.select_dtypes(include=['number']).columns
                
                if len(numeric_cols) > 0:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if len(numeric_cols) >= 1:
                            fig_bar = px.bar(df_results, x=df_results.columns[0], y=numeric_cols[0] if len(numeric_cols) > 0 else None)
                            st.plotly_chart(fig_bar, use_container_width=True)
                    
                    with col2:
                        if len(numeric_cols) >= 2:
                            fig_scatter = px.scatter(df_results, x=numeric_cols[0], y=numeric_cols[1])
                            st.plotly_chart(fig_scatter, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Sample queries
        if hasattr(st.session_state, 'show_samples') and st.session_state.show_samples:
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            st.header("💡 Sample Questions")
            
            sample_questions = [
                "Show me the first 10 rows of data",
                f"What are the unique values in the first column?",
                "Give me a summary of all numeric columns",
                "Show me the data types of all columns",
                "What is the total count of records?"
            ]
            
            for i, sample in enumerate(sample_questions):
                if st.button(f"Sample {i+1}: {sample}", key=f"sample_{i}"):
                    st.session_state.sample_question = sample
            
            if hasattr(st.session_state, 'sample_question'):
                st.info(f"Selected: {st.session_state.sample_question}")
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 