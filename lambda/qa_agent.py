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
    """QA Agent
    Listens for FeatureReady events and performs tests (simulated pass).
    Emits a TestPassed event after tests pass.
    """
    # Extract feature from incoming event detail
    feature = event.get('detail', {}).get('feature', 'unknown')
    # Simulate test passing and save result to context table
    table.put_item(Item={'id': 'last_test_feature', 'feature': feature, 'result': 'passed'})
    # Send a TestPassed event to the bus
    eventbridge.put_events(Entries=[{
        'Source': 'cloudswarm.qa',
        'DetailType': 'TestPassed',
        'Detail': json.dumps({'feature': feature}),
        'EventBusName': EVENT_BUS_NAME
    }])
    return {'status': 'TestPassed emitted'}
