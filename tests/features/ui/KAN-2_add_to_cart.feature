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
