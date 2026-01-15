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
    """Ops Agent
    Listens for TestPassed events and simulates deployment.
    Emits a Deployed event after deploying the feature.
    """
    feature = event.get('detail', {}).get('feature', 'unknown')
    # Simulate deployment and save to context table
    table.put_item(Item={'id': 'deployed_feature', 'feature': feature, 'status': 'deployed'})
    # Send a Deployed event to the bus
    eventbridge.put_events(Entries=[{
        'Source': 'cloudswarm.ops',
        'DetailType': 'Deployed',
        'Detail': json.dumps({'feature': feature}),
        'EventBusName': EVENT_BUS_NAME
    }])
    return {'status': 'Deployed emitted'}
