# 🤖 SQL Agent - Excel to SQL Query Generator

A powerful web application that allows you to upload Excel files and ask natural language questions to generate SQL queries and get data insights. Built with Streamlit and OpenAI's GPT models.

## ✨ Features

- **📁 Dynamic Excel Upload**: Upload any Excel file (.xlsx, .xls) and automatically convert it to a SQLite database
- **🤖 AI-Powered SQL Generation**: Use natural language to ask questions about your data
- **📊 Interactive Data Visualization**: Automatic charts and graphs for your query results
- **📋 Data Preview & Statistics**: View your data structure and basic statistics
- **💾 Export Results**: Download query results as CSV files
- **🎨 Modern UI**: Beautiful, responsive interface with intuitive design
- **🔍 Sample Queries**: Get inspiration with pre-built sample questions
- **📈 Real-time Analytics**: Instant SQL generation and execution

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd sql_agent_llm
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate sample data (optional)**
   ```bash
   python sample_data.py
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 📖 How to Use

### Step 1: Configure API Key
- Enter your Google Gemini API key in the sidebar
- The application uses Gemini 2.0 Flash for SQL generation

### Step 2: Upload Excel File
- Drag and drop your Excel file or click to browse
- Supported formats: `.xlsx`, `.xls`
- The file will be automatically converted to a SQLite database

### Step 3: Ask Questions
- Use natural language to ask questions about your data
- Examples:
  - "Show me the top 10 sales by region"
  - "What is the average salary by department?"
  - "Find all employees hired in 2023"
  - "Calculate total revenue by month"

### Step 4: View Results
- Generated SQL query is displayed with syntax highlighting
- Query results are shown in a data table
- Automatic visualizations are created for numeric data
- Download results as CSV if needed

## 🎯 Example Questions

### Sales Data
- "Show me the top 5 products by total sales"
- "What is the average order value by region?"
- "Find all orders above $1000"
- "Calculate monthly sales trends"

### Employee Data
- "Show me employees with salary above $80,000"
- "What is the average age by department?"
- "Find the highest paid employee in each department"
- "Show me employees hired in the last year"

### Customer Data
- "Which cities have the most customers?"
- "Show me customers who spent more than $5000"
- "What is the average order count per customer type?"
- "Find customers registered in 2023"

## 🏗️ Architecture

### Core Components

1. **Streamlit Web Interface** (`app.py`)
   - File upload handling
   - User interface and interactions
   - Data visualization
   - Results display

2. **SQL Agent** (`sql_agent.py`)
   - OpenAI integration for SQL generation
   - Database schema analysis
   - Query execution and validation
   - Natural language processing

3. **Data Processing**
   - Excel to SQLite conversion
   - Schema extraction
   - Sample data generation

### Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite
- **AI**: Google Gemini 2.0 Flash
- **Data Processing**: Pandas, SQLAlchemy
- **Visualization**: Plotly
- **Excel Handling**: OpenPyXL

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

### Customization Options

1. **Model Configuration**: Modify the model in `sql_agent.py`
   ```python
   self.llm = ChatGoogleGenerativeAI(
       model="gemini-2.0-flash",  # Change to gemini-2.0-exp for better results
       temperature=0,
       google_api_key=api_key
   )
   ```

2. **Database Settings**: Adjust database creation in `app.py`
   ```python
   engine = create_engine(f'sqlite:///{db_path}', echo=True)
   ```

3. **UI Customization**: Modify CSS styles in `app.py`

## 📊 Sample Data

The application includes sample data generation for testing:

- **Sales Data**: 1000 records with order details, regions, products
- **Employee Data**: 500 records with employee information, departments, salaries
- **Customer Data**: 300 records with customer profiles and order history

Run `python sample_data.py` to generate these files.

## 🛠️ Troubleshooting

### Common Issues

1. **Google Gemini API Key Error**
   - Ensure your API key is valid and has sufficient credits
   - Check if the key is entered correctly in the sidebar

2. **File Upload Issues**
   - Verify the Excel file is not corrupted
   - Check file format (.xlsx or .xls)
   - Ensure file size is reasonable (< 100MB)

3. **SQL Generation Errors**
   - Try rephrasing your question
   - Check if column names in your data match your question
   - Use the sample questions as reference
   - **Fixed**: SQL syntax errors with extra prefixes (like "ite") are now automatically cleaned

4. **Performance Issues**
   - Large files may take longer to process
   - Consider splitting large datasets
   - Use LIMIT in your questions for large result sets

### Error Messages

- **"Error reading file"**: Check file format and corruption
- **"Error executing SQL query"**: Review generated SQL syntax
- **"API Key not configured"**: Enter valid Google Gemini API key

### Recent Fixes

- **SQL Query Cleaning**: Enhanced the SQL cleaning function to automatically remove extra text prefixes that sometimes appear in LLM responses
- **Better Error Handling**: Improved validation to catch malformed SQL queries before execution
- **Enhanced Prompts**: Updated system prompts to generate cleaner SQL queries

## 🔒 Security Considerations

- API keys are stored in session state only
- Temporary database files are created for each session
- No data is permanently stored on the server
- Consider using environment variables for production

## 🚀 Deployment

### Local Deployment
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Cloud Deployment
The application can be deployed on:
- Streamlit Cloud
- Heroku
- AWS/GCP/Azure
- Docker containers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google for providing the Gemini models
- Streamlit for the web framework
- Pandas and SQLAlchemy for data processing
- Plotly for visualizations

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the example questions
3. Ensure your data format is correct
4. Verify your Google Gemini API key is valid

---

**Happy Querying! 🎉** 