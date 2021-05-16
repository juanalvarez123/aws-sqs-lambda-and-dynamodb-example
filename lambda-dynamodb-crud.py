import boto3
import logging
import json
import os

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.info('Loading function')
dynamodb_client = boto3.client('dynamodb')


def lambda_handler(event, context):
    operations = {
        'POST': lambda dynamo, x: dynamo.put_item(TableName=os.environ['DYNAMODB_TABLE'], Item=x),

        # TODO: Implement the rest of the methods
        # 'DELETE': lambda dynamo, x: dynamo.delete_item(...),
        # 'PUT': lambda dynamo, x: dynamo.update_item(...),
        # 'GET': lambda dynamo, x: dynamo.get_item(...),
        # 'GET_ALL': lambda dynamo, x: dynamo.scan(...),
    }

    logger.info('Starting ...')
    logger.info('Events: %s', event['Records'])

    for record in event['Records']:
        payload = json.loads(record['body'])
        logger.info('Payload: %s', payload)
        operation = record['messageAttributes']['Method']['stringValue']
        logger.info('Operation: %s', operation)

        if operation in operations:
            try:
                operations[operation](dynamodb_client, payload)
            except Exception as e:
                logger.error(e)
        else:
            logger.error('Unsupported method: %s', operation)
    return 0
