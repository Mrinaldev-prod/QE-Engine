Feature: Login (API)

  Scenario: Successful login via API
    Given a valid user payload
    When the client calls the POST /api/login endpoint
    Then the response status should be 200
    And the response should contain a token
