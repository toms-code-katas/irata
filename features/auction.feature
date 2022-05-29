Feature: Auctions as a means of trading goods

Scenario: Calculate food spoilage for players as half of his inventory units not consumed in the last turn
  Given I create the following players:
    | name     | type    |
    | A        | Flapper |
    | B        | Flapper |
  And the players have the following state for food:
    | name     | inventory | consumed in last turn |
    | A        | 3         | 3                     |
    | B        | 9         | 3                     |
  When I calculate the spoilage of food for player A
  And I calculate the spoilage of food for player B
  Then player A should have spoiled 0 units of food
  And player B should have spoiled 3 unit of food

Scenario: Calculate smithore spoilage for players as all units in inventory above 50
  Given I create the following players:
    | name     | type    |
    | A        | Flapper |
    | B        | Flapper |
  And the players have the following state for food:
    | name     | inventory | consumed in last turn |
    | A        | 49        | 0                     |
    | B        | 51        | 0                     |
  When I calculate the spoilage of smithore for player A
  And I calculate the spoilage of smithore for player B
  Then player A should have spoiled 0 units of smithore
  And player B should have spoiled 1 unit of smithore

