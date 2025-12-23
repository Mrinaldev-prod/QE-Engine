Feature: Login (Web UI)

  Scenario: Successful login
    Given the user opens the login page
    When the user submits valid credentials
    Then the user should be redirected to the home page
