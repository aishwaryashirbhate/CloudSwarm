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
    """Developer Agent
    Receives feature requests via EventBridge and saves the feature description in DynamoDB.
    Emits a FeatureReady event after storing context.
    """
    # Extract feature from incoming event detail
    feature = event.get('detail', {}).get('feature', 'unknown')
    # Save the current feature to the context table
    table.put_item(Item={'id': 'current_feature', 'feature': feature})
    # Send a FeatureReady event to the bus
    eventbridge.put_events(Entries=[{
        'Source': 'cloudswarm.dev',
        'DetailType': 'FeatureReady',
        'Detail': json.dumps({'feature': feature}),
        'EventBusName': EVENT_BUS_NAME
    }])
    return {'status': 'FeatureReady emitted'}
