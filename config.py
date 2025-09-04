"""
Configuration helper for BigQuery Agent
Use this to set up your API key and table names in BigQuery notebooks
"""

import os

def setup_config(gemini_api_key: str, bigquery_tables: list = None):
    """
    Set up configuration for the BigQuery agent in a notebook environment.
    
    Args:
        gemini_api_key (str): Your Gemini API key
        bigquery_tables (list, optional): List of BigQuery table names to work with
                                        Format: ["project.dataset.table", ...]
    
    Example usage in BigQuery notebook:
        from config import setup_config
        setup_config(
            gemini_api_key="AIza...",
            bigquery_tables=["your-project.your_dataset.your_table"]
        )
    """
    # Set environment variables
    os.environ['GOOGLE_API_KEY'] = gemini_api_key
    os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = '0'
    
    if bigquery_tables:
        os.environ['BIGQUERY_TABLES'] = ','.join(bigquery_tables)
    
    print(f"✅ Configuration set:")
    print(f"   - Gemini API key configured")
    print(f"   - BigQuery tables: {bigquery_tables or 'None specified (will explore all available)'}")
    print()
    print("Now you can import and run your agent:")
    print("   from greeting_agent.agent import root_agent")
    print("   # Agent is ready to use!")

def get_current_config():
    """Get the current configuration."""
    return {
        'gemini_api_key_set': bool(os.getenv('GOOGLE_API_KEY')),
        'bigquery_tables': os.getenv('BIGQUERY_TABLES', '').split(',') if os.getenv('BIGQUERY_TABLES') else [],
        'use_vertex_ai': os.getenv('GOOGLE_GENAI_USE_VERTEXAI', '0') == '1'
    }

# Quick setup function for single table
def quick_setup_single_table(gemini_api_key: str, table_name: str):
    """
    Quick setup for working with a single table.
    
    Args:
        gemini_api_key (str): Your Gemini API key
        table_name (str): Full BigQuery table name (project.dataset.table)
    """
    setup_config(
        gemini_api_key=gemini_api_key,
        bigquery_tables=[table_name]
    )
    print(f"🎯 Quick setup complete for table: {table_name}")