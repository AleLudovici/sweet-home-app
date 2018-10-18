# put_expense_handler_tests.py

import boto3
from moto import mock_dynamodb2
from src.put_expense_handler import put_expense_handler


@mock_dynamodb2
def test_handler_adds_expense_in_dynamodb():
    set_up_dynamodb()
    put_expense_handler(api_gateway_object_created_event(), None)
    table = boto3.resource('dynamodb').Table('expenses')
    item = table.get_item(Key={'expense_id': 0})['Item']
    expected = api_gateway_object_created_event()
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
    response = put_expense_handler(api_gateway_object_created_event(), None)
    assert response == {'status_code': 201}


def test_handler_when_throws_an_exception_returns_400():
    response = put_expense_handler(api_gateway_object_created_event(), None)
    assert response['status_code'] == 400


@mock_dynamodb2
def test_handler_returns_404_when_expense_already_exists():
    set_up_dynamodb()

    expected_positive = {"status_code": 201}
    expected_negative = {
                "status_code": 404,
                "reason": 'An expense with the same ID already exists'
            }

    actual_positive = put_expense_handler(api_gateway_object_created_event(), None)
    actual_negative = put_expense_handler(api_gateway_object_created_event(), None)
    assert actual_positive == expected_positive and actual_negative == expected_negative


def set_up_dynamodb():
    client = boto3.client('dynamodb')
    client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'expense_id',
                'AttributeType': 'N'
            }
        ],
        TableName='expenses',
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
    # NOTE: truncated event object shown here
    return {
        "id": 0,
        "date": "2018-16-10",
        "amount": 10.5,
        "currency": "£",
        "user": {
            "id": 0,
            "name": "Alessandro",
            "last_name": "Ludovici"
        },
        "location": {
            "name": "Bakery",
            "description": "bread"
        }
    }
