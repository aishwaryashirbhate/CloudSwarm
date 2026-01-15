import os
import json
import boto3

# Simple utility functions for AI-centric CloudSwarm features

dynamodb = boto3.resource('dynamodb')
# Use VECTOR_TABLE if set, else fall back to context table
TABLE_NAME = os.environ.get('VECTOR_TABLE', os.environ.get('CONTEXT_TABLE', ''))

def store_embedding(key, embedding):
    """
    Store an embedding vector in the DynamoDB table.
    Embedding should be a list of floats. We serialize to JSON for storage.
    """
    table = dynamodb.Table(TABLE_NAME)
    # ensure key is string
    item = {
        'pk': str(key),
        'vector': json.dumps(embedding)
    }
    table.put_item(Item=item)
    return True

def retrieve_similar(query_embedding, top_k=3):
    """
    Retrieve similar embeddings. This is a placeholder implementation.
    In a real system, you would query a vector database or perform a nearest-neighbor search.
    """
    # Placeholder: return empty list
    return []

def select_model(task_type):
    """
    Select an appropriate model for a given task.
    This function can be extended to implement dynamic model selection based on task complexity.
    """
    # Map of task types to preferred models (this can come from environment variables)
    model_map = {
        'code_generation': os.environ.get('CODE_MODEL', os.environ.get('DEFAULT_MODEL', 'anthropic.claude-v2')),
        'analysis': os.environ.get('ANALYSIS_MODEL', os.environ.get('DEFAULT_MODEL', 'anthropic.claude-v2')),
        'qa': os.environ.get('QA_MODEL', os.environ.get('DEFAULT_MODEL', 'anthropic.claude-v2')),
        'ops': os.environ.get('OPS_MODEL', os.environ.get('DEFAULT_MODEL', 'anthropic.claude-v2'))
    }
    return model_map.get(task_type, os.environ.get('DEFAULT_MODEL', 'anthropic.claude-v2'))
