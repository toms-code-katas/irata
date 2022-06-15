Feature: Calculation of surplus and spoilage

Scenario: Calculate food spoilage for players as half of his inventory units not consumed in the last turn (rounded up)
  Given I create the following players
    | name     | type    |
    | A        | Flapper |
    | B        | Flapper |
  And the players have the following state for food
    | name     | previous amount | usage |
    | A        | 3               | 3     |
    | B        | 9               | 3     |
  When I calculate the spoilage of food for player A
  And I calculate the spoilage of food for player B
  Then player A should have spoiled 0 units of food
  And player B should have spoiled 3 unit of food

Scenario: Calculate smithore spoilage for players as all units in inventory above 50
  Given I create the following players
    | name     | type    |
    | A        | Flapper |
    | B        | Flapper |
  And the players have the following state for smithore
    | name     | previous amount | usage |
    | A        | 49              | 0     |
    | B        | 51              | 0     |
  When I calculate the spoilage of smithore for player A
  And I calculate the spoilage of smithore for player B
  Then player A should have spoiled 0 units of smithore
  And player B should have spoiled 1 unit of smithore


Scenario: Calculate food surplus / shortage for players
  Given I create the following players
    | name     | type    |
    | A        | Flapper |
    | B        | Flapper |
    | C        | Flapper |
  And the players have the following state for food
    | name     | previous amount | usage | production |
    | A        | 3               | 3     | 1          |
    | B        | 6               | 3     | 2          |
    | C        | 15              | 3     | 0          |
  When I calculate the spoilage of food for all players
  And I calculate the surplus / shortage of food for all players
  Then player A should have a shortage of 2 units of food
  Then player B should have a shortage of 0 units of food
  Then player C should have a surplus of 3 units of food

Scenario: Calculate energy surplus / shortage for players which is the number of plots owned plus one
  Given I create a default map
  And I finish map creation
  And I create the following players
    | name     | type    |
    | A        | Flapper |
    | B        | Flapper |
    | C        | Flapper |
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
  When I calculate the spoilage of energy for all players
  And I calculate the surplus / shortage of energy for all players
  Then player A should have a shortage of 2 units of energy
  Then player B should have a shortage of 0 units of energy
  Then player C should have a surplus of 3 units of energy
