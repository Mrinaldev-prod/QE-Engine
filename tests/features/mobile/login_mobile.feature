Feature: Login (Mobile)

  Scenario: Successful login on mobile
    Given the mobile app is launched
    When the user logs in with valid credentials
    Then the user sees the dashboard screen
