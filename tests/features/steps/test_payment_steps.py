import json

import pytest

from pytest_bdd import scenario, given, then, when
from starlette import status
from starlette.testclient import TestClient

from src.app import app
from tests.utils.payment_helper import PaymentHelper

client = TestClient(app)


@pytest.fixture
def generate_payment_dto():
    return PaymentHelper.generate_payment_request()


@pytest.fixture
def generate_multiple_payment_dtos():
    return PaymentHelper.generate_multiple_payments()


@pytest.fixture
def request_payment_creation(generate_payment_dto):
    payment = generate_payment_dto
    req_body = {
        "order_id": str(payment.order_id),
    }
    headers = {}
    response = client.post("/payments", json=req_body, headers=headers)

    resp_json = json.loads(response.content)
    result = resp_json["result"]
    order_id = result["orderId"]

    yield response
    # Teardown - Removes the customer from the database
    client.delete(f"/payments/{order_id}", headers=headers)


@pytest.fixture
def request_multiple_payments_creation(generate_multiple_payment_dtos):
    payment_list = generate_multiple_payment_dtos
    payment_ids_list = []
    headers = {}

    for payment in payment_list:
        req_body = {
            "orderId": str(payment.order_id)
        }
        response = client.post("/payments", json=req_body, headers=headers)

        resp_json = json.loads(response.content)
        result = resp_json["result"]
        order_id = result["orderId"]
        payment_ids_list.append(order_id)
    yield payment_ids_list
    # Teardown - Removes the customer from the database
    for order_id in payment_ids_list:
        client.delete(f"/payments/{order_id}", headers=headers)


@pytest.fixture
def create_payment_without_teardown(generate_payment_dto):
    payment = generate_payment_dto
    req_body = {
        "order_id": str(payment.order_id),
    }
    headers = {}
    response = client.post("/payments", json=req_body, headers=headers)
    yield response.content


# Scenario: Create a new payment


@scenario('../payment.feature', 'Create a new payment')
def test_create_payment():
    pass


@given('I submit a new payment data', target_fixture='i_request_to_create_a_new_payment_impl')
def i_request_to_create_a_new_payment_impl(generate_payment_dto, request_payment_creation):
    response = request_payment_creation
    return response


@then('the payment should be created successfully')
def the_payment_should_be_created_successfully_impl(i_request_to_create_a_new_payment_impl, generate_payment_dto):
    payment = generate_payment_dto

    resp_json = json.loads(i_request_to_create_a_new_payment_impl.content)
    result = resp_json["result"]

    assert result["orderId"] == str(payment.order_id)


# Scenario: Get payment by ID

@scenario('../payment.feature', 'Get payment by order ID')
def test_get_payment_by_id():
    pass


@given('there is a payment with an order ID', target_fixture='payment_with_given_id')
def payment_with_given_id(request_payment_creation):
    response = request_payment_creation
    resp_json = json.loads(response.content)
    result = resp_json["result"]
    return result["orderId"]


@when('I request to get the payment by order ID', target_fixture='request_payment_by_id')
def request_payment_by_id(payment_with_given_id):
    order_id = payment_with_given_id
    headers = {}
    response = client.get(f"/payments/id/{order_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('I should receive the payment details by order ID')
def receive_correct_payment(payment_with_given_id, request_payment_by_id, generate_payment_dto):
    order_id = payment_with_given_id
    payment = generate_payment_dto
    resp_json = json.loads(request_payment_by_id)
    result = resp_json["result"]

    assert result["orderId"] == order_id


# Scenario: Get all payments

@scenario('../payment.feature', 'Get all payments')
def test_get_all_payments():
    pass


@given('there are existing payments in the system', target_fixture='existing_payments_in_db')
def existing_customers_in_db(request_multiple_payments_creation):
    payments_id_list = request_multiple_payments_creation
    return payments_id_list


@when('I request to get all payments', target_fixture='request_all_payments')
def request_all_payments():
    headers = {}
    response = client.get(f"/payments/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('I should receive a list of payments')
def receive_correct_customer(existing_payments_in_db, request_all_payments):
    payments_id_list = existing_payments_in_db
    response = request_all_payments
    resp_json = json.loads(response)
    result = resp_json["result"]

    assert type(result) == list

    for item in result:
        assert item["orderId"] in payments_id_list


# Scenario: Remove a payment

@scenario('../payment.feature', 'Remove a payment')
def test_remove_payment():
    pass


@given('there is a payment on database with specific order id', target_fixture='existing_payment_to_remove')
def existing_payment_to_remove(create_payment_without_teardown):
    payment = create_payment_without_teardown
    return payment


@when('I request to remove a payment', target_fixture='request_payment_update')
def request_payment_delete(existing_payment_to_remove):
    response = existing_payment_to_remove
    resp_json = json.loads(response)
    result = resp_json["result"]
    order_id = result["orderId"]

    headers = {}
    response = client.delete(f"/payments/{order_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('the payment data is successfully removed')
def receive_correct_payment(existing_payment_to_remove):
    response = existing_payment_to_remove
    resp_json = json.loads(response)
    result = resp_json["result"]
    order_id = result["orderId"]

    headers = {}
    response = client.get(f"/payments/id/{order_id}", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
