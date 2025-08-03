#!/usr/bin/env python3
"""
Test script for Gemini API integration
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

def test_gemini_connection():
    """Test the Gemini API connection"""
    print("🧪 Testing Gemini API Connection...")
    
    # Your API key
    api_key = ""
    
    try:
        # Initialize Gemini model
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            google_api_key=api_key
        )
        
        # Test with a simple prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Generate a simple SQL query."),
            ("human", "Create a SQL query to select all records from a table called 'users'")
        ])
        
        chain = prompt | llm
        
        response = chain.invoke({})
        
        print("✅ Gemini API connection successful!")
        print(f"📝 Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to Gemini API: {e}")
        return False

if __name__ == "__main__":
    test_gemini_connection() 
