import requests
from behave import given, when, then


@given('a valid user payload')
def valid_payload(context):
    context.payload = {'email': 'test@example.com', 'password': 'Password123!'}


@when('the client calls the POST /api/login endpoint')
def call_login(context):
    base = context.config.userdata.get('api_base', 'https://api.example.com')
    context.response = requests.post(f"{base}/api/login", json=context.payload)


@then('the response status should be 200')
def check_status(context):
    assert context.response.status_code == 200


@then('the response should contain a token')
def response_has_token(context):
    data = context.response.json()
    assert 'token' in data
