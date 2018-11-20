# put_expense_handler_tests.py

import boto3
import mock
import os
import json
from moto import mock_dynamodb2
from src.handler import create_expense


@mock_dynamodb2
def test_handler_adds_expense_in_dynamodb():
    set_up_dynamodb()
    create_expense(api_gateway_object_created_event(), None)
    table = boto3.resource('dynamodb').Table(os.environ['tableName'])
    item = table.get_item(Key={'expense_id': 0})['Item']
    expected = json.loads(api_gateway_object_created_event()['body'])
    assert item['expense_id'] == expected['id']
    assert item['date'] == expected['date']
    assert item['amount'] == expected['amount']
    assert item['currency'] == expected['currency']
    assert item['user']['user_id'] == expected['user']['id']
    assert item['user']['name'] == expected['user']['name']
    assert item['user']['last_name'] == expected['user']['last_name']
    assert item['location']['name'] == expected['location']['name']
    assert item['location']['description'] == expected['location']['description']


@mock_dynamodb2
def test_handler_when_adds_expense_in_dynamodb_succeed_returns_201():
    set_up_dynamodb()
    response = create_expense(api_gateway_object_created_event(), None)
    assert response == {'statusCode': 201}


def test_handler_when_throws_an_exception_returns_400():
    response = create_expense(api_gateway_object_created_event(), None)
    assert response['statusCode'] == 400


@mock_dynamodb2
def test_handler_returns_404_when_expense_already_exists():
    set_up_dynamodb()

    expected_positive = {"statusCode": 201}
    expected_negative = {
                "statusCode": 404,
                "body": 'An expense with the same ID already exists'
            }

    actual_positive = create_expense(api_gateway_object_created_event(), None)
    actual_negative = create_expense(api_gateway_object_created_event(), None)
    assert actual_positive == expected_positive and actual_negative == expected_negative


def set_up_dynamodb():
    table_name = mock.patch.dict(os.environ, {'tableName': 'testTable'})
    table_name.start()
    client = boto3.client('dynamodb')
    client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'expense_id',
                'AttributeType': 'N'
            }
        ],
        TableName=os.environ['tableName'],
        KeySchema=[
            {
                'AttributeName': 'expense_id',
                'KeyType': 'HASH'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )


def api_gateway_object_created_event():
    event = open('test_lambda_event.json').read()
    test_json = json.loads(event)
    return test_json
