from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.cloud import bigquery
import os

# Configuration - can be overridden in notebook environment
GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
CONFIGURED_TABLES = os.getenv('BIGQUERY_TABLES', '').split(',') if os.getenv('BIGQUERY_TABLES') else []

# Initialize BigQuery client (will use default credentials in notebook environment)
def get_bigquery_client():
    try:
        return bigquery.Client()
    except Exception:
        # Return None if not in authenticated environment (for testing)
        return None

# Helper functions for configured tables
def get_configured_tables():
    """Get the list of configured BigQuery tables."""
    if CONFIGURED_TABLES and CONFIGURED_TABLES != ['']:
        return CONFIGURED_TABLES
    return []

def parse_table_name(table_name):
    """Parse a full table name into project, dataset, and table components."""
    parts = table_name.split('.')
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]  # project, dataset, table
    elif len(parts) == 2:
        return None, parts[0], parts[1]  # dataset, table (use default project)
    else:
        return None, None, parts[0]  # just table name

# BigQuery Tools
def list_datasets():
    """List all datasets in the current project, including configured tables if specified."""
    client = get_bigquery_client()
    if not client:
        return "BigQuery client not available. Run this in a BigQuery notebook environment."
    
    result = {}
    
    # Add configured tables if specified
    configured_tables = get_configured_tables()
    if configured_tables:
        result["configured_tables"] = configured_tables
        result["message"] = "These are your configured BigQuery tables. You can also explore other datasets."
    
    try:
        datasets = list(client.list_datasets())
        if not datasets and not configured_tables:
            return "No datasets found in the current project."
        
        dataset_info = []
        for dataset in datasets:
            dataset_info.append({
                "dataset_id": dataset.dataset_id,
                "full_name": f"{dataset.project}.{dataset.dataset_id}"
            })
        result["datasets"] = dataset_info
        return result
    except Exception as e:
        if configured_tables:
            return {"configured_tables": configured_tables, "error": f"Error listing datasets: {str(e)}"}
        return f"Error listing datasets: {str(e)}"

def list_tables(dataset_id: str):
    """List all tables in a specific dataset."""
    client = get_bigquery_client()
    if not client:
        return "BigQuery client not available. Run this in a BigQuery notebook environment."
    
    try:
        dataset_ref = client.dataset(dataset_id)
        tables = list(client.list_tables(dataset_ref))
        
        if not tables:
            return f"No tables found in dataset {dataset_id}."
        
        table_info = []
        for table in tables:
            table_info.append({
                "table_id": table.table_id,
                "full_name": f"{table.project}.{table.dataset_id}.{table.table_id}",
                "table_type": table.table_type
            })
        return {"tables": table_info}
    except Exception as e:
        return f"Error listing tables in dataset {dataset_id}: {str(e)}"

def get_table_schema(table_name: str):
    """Get the schema information for a specific table. 
    
    Args:
        table_name: Can be full name (project.dataset.table) or dataset.table or just table
    """
    client = get_bigquery_client()
    if not client:
        return "BigQuery client not available. Run this in a BigQuery notebook environment."
    
    try:
        # Parse the table name
        project, dataset, table = parse_table_name(table_name)
        
        # If no project specified, use client's project
        if not project:
            project = client.project
        
        # If no dataset specified, try to find it from configured tables
        if not dataset:
            configured_tables = get_configured_tables()
            for configured_table in configured_tables:
                if table in configured_table:
                    _, dataset, _ = parse_table_name(configured_table)
                    break
            if not dataset:
                return f"Cannot determine dataset for table '{table}'. Please provide full table name (project.dataset.table) or configure BIGQUERY_TABLES."
        
        table_ref = client.dataset(dataset, project=project).table(table)
        table_obj = client.get_table(table_ref)
        
        schema_info = []
        for field in table_obj.schema:
            schema_info.append({
                "name": field.name,
                "type": field.field_type,
                "mode": field.mode,
                "description": field.description or ""
            })
        
        return {
            "table": f"{table_obj.project}.{table_obj.dataset_id}.{table_obj.table_id}",
            "num_rows": table_obj.num_rows,
            "schema": schema_info
        }
    except Exception as e:
        return f"Error getting schema for {table_name}: {str(e)}"

def execute_query(sql: str, max_rows: int = 1000):
    """Execute a SQL query and return the results."""
    client = get_bigquery_client()
    if not client:
        return "BigQuery client not available. Run this in a BigQuery notebook environment."
    
    try:
        # Add LIMIT if not present and max_rows is specified
        if max_rows and "LIMIT" not in sql.upper():
            sql = f"{sql.rstrip(';')} LIMIT {max_rows}"
        
        query_job = client.query(sql)
        results = query_job.result()
        
        # Convert to list of dictionaries
        rows = []
        for row in results:
            rows.append(dict(row))
        
        return {
            "query": sql,
            "row_count": len(rows),
            "rows": rows
        }
    except Exception as e:
        return f"Error executing query: {str(e)}"

# Create tool instances
list_datasets_tool = FunctionTool(list_datasets)
list_tables_tool = FunctionTool(list_tables)
get_table_schema_tool = FunctionTool(get_table_schema)
execute_query_tool = FunctionTool(execute_query)

root_agent = Agent(
    name="bigquery_data_agent",
    model="gemini-2.0-flash",
    description="BigQuery data analysis agent that answers questions about data using SQL queries",
    instruction="""
    You are an expert data analyst with access to BigQuery datasets and tables.
    
    Your capabilities include:
    - Exploring available datasets and tables
    - Understanding table schemas and data types
    - Writing and executing SQL queries to answer data questions
    - Providing insights and analysis based on query results
    - Explaining query logic and results in clear, business-friendly language
    
    When a user asks a question about data:
    1. First, explore the available datasets and tables to understand what data is available
    2. Examine table schemas to understand the structure and relationships
    3. Write appropriate SQL queries to answer the question
    4. Execute the queries and analyze the results
    5. Provide clear explanations of your findings
    
    Always be thorough in your analysis and explain your reasoning.
    If you need clarification about what data the user is interested in, ask specific questions.
    """,
    tools=[
        list_datasets_tool,
        list_tables_tool,
        get_table_schema_tool,
        execute_query_tool
    ]
)
