Feature: Auctions for energy

Background:
  Given I create a default map
  And I finish map creation
  And I create the following players
    | name     | type    | money |
    | A        | Flapper | 1000  |
    | B        | Flapper | 40    |
    | C        | Flapper | 100   |
  And the players own the following plots
    | name | x | y |
    | A    | 1 | 1 |
    | A    | 2 | 1 |
    | B    | 1 | 2 |
    | B    | 2 | 2 |
    | B    | 3 | 2 |
  And the players have the following state for energy
    | name     | previous amount | usage | production |
    | A        | 2               | 2     | 1          |
    | B        | 6               | 3     | 3          |
    | C        | 0               | 0     | 4          |
  And I create a store with the following inventory
    | resource | in stock | ask price | bid price |
    | energy   | 10       | 60        | 25        |
  When I calculate the spoilage of energy for all players
  And I calculate the surplus / shortage of energy for all players
  When I create an auction for energy
  And I start the auction
  Then player A should be a buyer
  Then player B should be a buyer
  Then player C should be a seller

Scenario: Basic energy auction
  When player A raises his bid price to 40
  And player C reduces his ask price to 40
  Then player A and player C should start trading
  When player A and player C trade 1 unit
  And player A reduces his bid price to 39
  Then player A and player C should stop trading
  And the players should have the following state for energy
    | name     | current amount  |
    | A        | 2               |
    | C        | 3               |
  And player A should have 960 units of money
  And player C should have 140 units of money

Scenario: Energy auction with seller reset after reaching critical level
  When player A raises his bid price to 40
  And player C reduces his ask price to 40
  Then player A and player C should start trading
  When player A and player C trade 3 units
  Then player A and player C should stop trading
  And player C's ask price should be reset
  And the players should have the following state for energy
    | name     | current amount  |
    | A        | 4               |
    | C        | 1               |
  And player A should have 880 units of money
  And player C should have 220 units of money

Scenario: Energy auction with seller inactive after running dry
  When player A raises his bid price to 40
  And player C reduces his ask price to 40
  Then player A and player C should start trading
  When player A and player C trade 3 units
  Then player A and player C should stop trading
  And player C's ask price should be reset
  When player C reduces his ask price to 40
  And player A and player C trade 1 units
  Then player A and player C should stop trading
  And player C should not be able to reduce his ask price to 60
  And the players should have the following state for energy
    | name     | current amount  |
    | A        | 5               |
    | C        | 0               |

Scenario: Energy auction with buyer stuck at bid price because of having insufficient funds
  Then player B should not be able to raise his bid price to 41
  When player C reduces his ask price to 30
  And player B raises his bid price to 30
  Then player C and player B should start trading
  When player C and player B trade 1 unit
  Then player C and player B should stop trading
  And player B's bid price should be reset
