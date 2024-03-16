Feature: Payment Management

  Scenario: Create a new payment
    Given I submit a new payment data
    Then the payment should be created successfully

  Scenario: Get payment by order ID
    Given there is a payment with an order ID
    When I request to get the payment by order ID
    Then I should receive the payment details by order ID

  Scenario: Get all payments
    Given there are existing payments in the system
    When I request to get all payments
    Then I should receive a list of payments

  Scenario: Remove a payment
    Given there is a payment on database with specific order id
    When I request to remove a payment
    Then the payment data is successfully removed