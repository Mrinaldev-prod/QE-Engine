Feature: KAN-2 — Add product to cart
  As a QE
  I should be able to navigate to Swab Labs inventory
  So that I can add the "Sauce Labs Backpack" to the cart

  Background:
    Given the user is logged in as "standard_user" with password "secret_sauce"

  @happy-path
  Scenario: Add Sauce Labs Backpack to the cart
    When I add "Sauce Labs Backpack" to the cart
    Then the shopping cart badge should show "1"
    And the product "Sauce Labs Backpack" should show a Remove button

  @negative
  Scenario: Unauthenticated user cannot access inventory
    Given the user is not logged in
    When the user navigates to the inventory page
    Then they should be redirected to the login page

  @negative
  Scenario: Attempt to add a nonexistent product does not change cart
    Given the user is logged in as "standard_user" with password "secret_sauce"
    When I attempt to add "Nonexistent Item" to the cart
    Then the shopping cart badge should show "0"
    And I should see no add-to-cart button for "Nonexistent Item"

  @negative
  Scenario: Locked out user cannot login
    Given the user attempts to login as "locked_out_user" with password "secret_sauce"
    Then I should see a login error message
