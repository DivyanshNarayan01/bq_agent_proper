# BigQuery Data Agent

A powerful AI agent built with Google's Agent Development Kit (ADK) for analyzing BigQuery data through natural language queries.

## Features

- **Natural Language to SQL**: Ask questions in plain English and get SQL queries executed automatically
- **Schema Exploration**: Automatically discovers and understands your BigQuery datasets and tables
- **Data Analysis**: Provides insights and explanations based on query results
- **BigQuery Native**: Optimized for BigQuery notebook environments with automatic authentication

## Quick Start in BigQuery Notebook

### Method 1: Secure Setup (Recommended)

1. **Clone this repository**:
   ```bash
   git clone <your-repo-url>
   cd bq_agent_proper
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure securely in notebook**:
   ```python
   import os
   import getpass
   
   # Securely input your API key (won't be displayed)
   print("Enter your Gemini API key:")
   api_key = getpass.getpass("API Key: ")
   os.environ['GOOGLE_API_KEY'] = api_key
   
   # Optional: Set BigQuery tables
   tables = input("Enter BigQuery tables (optional): ").strip()
   os.environ['BIGQUERY_TABLES'] = tables
   
   # Add current directory to Python path and import agent
   import sys
   if os.getcwd() not in sys.path:
       sys.path.insert(0, os.getcwd())
   
   from greeting_agent.agent import root_agent
   
   # Start asking questions!
   response = root_agent.run("What datasets are available?")
   print(response)
   ```

### Method 2: Using Secure Configuration Helper

```python
from config import secure_setup

# This will prompt for your API key securely (input won't be displayed)
secure_setup()

from greeting_agent.agent import root_agent
# Agent is ready to use!
```

### Method 3: Full Setup Script

```bash
./setup.sh
adk run greeting_agent
```

## What the Agent Can Do

- **Explore Data**: "What datasets are available?" or "What tables are in [dataset]?"
- **Understand Schema**: "What columns are in [table_name]?"
- **Run Analysis**: "Show me the first 10 rows of [table_name]" or "How many records are in [table_name]?"
- **Generate Insights**: "What are the unique values in [column_name]?" or "Show me summary statistics"

## Example Usage

```
You: "What datasets are available?"
Agent: I found several datasets in your project. Let me show you what's available...

You: "What columns are in my_table?"
Agent: Let me get the schema for your table...

You: "Show me a sample of the data"
Agent: I'll run a query to show you the first few rows...
```

## Architecture

- **Agent Core**: `greeting_agent/agent.py` - Main agent configuration
- **BigQuery Tools**: Automatic access to BigQuery datasets, tables, and query execution
- **Authentication**: Uses BigQuery notebook's built-in authentication (no setup required)

## Dependencies

- Google ADK with BigQuery support
- Google Cloud BigQuery libraries
- Standard data analysis libraries (pandas, numpy, matplotlib)

## Development

The agent uses ADK's BigQuery toolset which includes:
- `list_dataset_ids` - Discover available datasets
- `get_dataset_info` - Get dataset metadata
- `list_table_ids` - Find tables in datasets
- `get_table_info` - Understand table schemas
- `execute_sql` - Run SQL queries and return results

## Troubleshooting

If you encounter issues:
1. Ensure you're running in a BigQuery notebook environment
2. Check that BigQuery API is enabled in your project
3. Verify the agent has access to your datasets

## Next Steps

Once running, try asking:
- "What data do I have available?"
- "Show me a sample from the [table_name] table"
- "What are the most recent records in [table_name]?"