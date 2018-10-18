# handler.py
import boto3
import logging
from botocore.exceptions import ClientError
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def put(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('expenses')
        table.put_item(
            Item={
                'expense_id': event['id'],
                'date': event['date'],
                'amount': Decimal(event['amount']),
                'currency': event['currency'],
                'user': {
                    'user_id': event['user']['id'],
                    'name': event['user']['name'],
                    'last_name': event['user']['last_name']
                },
                'location': {
                    'name': event['location']['name'],
                    'description': event['location']['description']
                }
            }
        )
        return {
            "status_code": 201
        }

    except ClientError as error:
        logger.error("Unexpected error: %s", error, exc_info=True)

        return {
            "status_code": 500
        }