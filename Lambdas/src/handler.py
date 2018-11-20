# handler.py
import boto3
import logging
import os
import json
from botocore.exceptions import ClientError
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_expense(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['tableName'])
        expense = json.loads(event['body'])
        table.put_item(
            Item={
                'expense_id': expense['id'],
                'date': expense['date'],
                'amount': Decimal(expense['amount']),
                'currency': expense['currency'],
                'user': {
                    'user_id': expense['user']['id'],
                    'name': expense['user']['name'],
                    'last_name': expense['user']['last_name']
                },
                'location': {
                    'name': expense['location']['name'],
                    'description': expense['location']['description']
                }
            },
            ConditionExpression='attribute_not_exists(expense_id)'
        )
        return {
            "statusCode": 201,
        }

    except ClientError as error:
        logger.error("Unexpected error: %s", error, exc_info=True)

        if error.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {
                "statusCode": 404,
                "body": 'An expense with the same ID already exists'
            }
        else:
            return {
                "statusCode": error.response['ResponseMetadata']['HTTPStatusCode'],
                "body": error.response['Error']['Message']
            }
