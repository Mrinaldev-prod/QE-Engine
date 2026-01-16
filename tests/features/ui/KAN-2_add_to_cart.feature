Feature: KAN-2 — Add item to cart from inventory
  As a QE
  I should be able to navigate to the Swab Labs inventory page
  So that I can add the Sauce Labs Backpack to the cart

  Background:
    Given the browser is on the inventory page
      # Inventory URL: https://www.saucedemo.com/inventory.html

  @happy-path
  Scenario: Add Sauce Labs Backpack to cart
    When I add the "Sauce Labs Backpack" to cart
    Then the cart count should be "1"
    And the cart should contain "Sauce Labs Backpack"
