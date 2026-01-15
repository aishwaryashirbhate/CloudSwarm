import json
import os
import boto3

# Initialize AWS clients
eventbridge = boto3.client('events')
dynamodb = boto3.resource('dynamodb')

# Environment variables for context table and event bus
CONTEXT_TABLE = os.environ.get('CONTEXT_TABLE')
EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME')

table = dynamodb.Table(CONTEXT_TABLE)

def lambda_handler(event, context):
    """Business Agent
    Listens for Deployed events and runs analysis; sends AnalysisComplete event.
    """
    feature = event.get('detail', {}).get('feature', 'unknown')
    # Simulate analysis and save result to context table
    table.put_item(Item={'id': 'analysis_feature', 'feature': feature, 'analysis': 'completed'})
    # Send an AnalysisComplete event to the bus
    eventbridge.put_events(Entries=[{
        'Source': 'cloudswarm.biz',
        'DetailType': 'AnalysisComplete',
        'Detail': json.dumps({'feature': feature}),
        'EventBusName': EVENT_BUS_NAME
    }])
    return {'status': 'AnalysisComplete emitted'}
