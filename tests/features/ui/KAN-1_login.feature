Feature: KAN-1 — User login
  As a user of the application
  I want to be able to authenticate successfully
  So that I can access the protected inventory pages

  Background:
    Given the browser is on the login page
      # The login page URL is: https://www.saucedemo.com/

  @happy-path
  Scenario Outline: Successful login with valid credentials
    When I enter username "<username>" and password "<password>"
    And I submit the login form
    Then I should be taken to the inventory page
    And I should see the products list

    Examples:
      | username      | password     |
      | standard_user | secret_sauce |

  @negative
  Scenario Outline: Unsuccessful login with invalid credentials
    When I enter username "<username>" and password "<password>"
    And I submit the login form
    Then I should remain on the login page
    And I should see a login error message

    Examples:
      | username     | password     |
      | locked_out_user | secret_sauce |
      | invalid_user  | wrong_pass   |
