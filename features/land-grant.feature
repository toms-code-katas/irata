Feature: Land grants let players choose a plot from the map

Scenario: Land grant general process
  Given I create a default map
  And I finish map creation
  And I create a land grant with the current map
  When I start the land grant
  Then the state of the land grant should be ongoing
  Then the current plot should contain the following attributes:
    | x | y | type   | state | owner |
    | 1 | 1 | plains | free  |       |
  When I advance the land grant 4 times
  Then the current plot should contain the following attributes:
    | x | y | type  | state | owner |
    | 5 | 1 | river | free  |       |
  When I advance the land grant 18 times
  Then the current plot should contain the following attributes:
    | x | y | type  | state  | owner  |
    | 5 | 3 | store | taken  | system |
  When I advance the land grant 22 times
  Then the current plot should contain the following attributes:
    | x | y | type   | state  | owner  |
    | 9 | 5 | plains | free   |        |
  When I advance the land grant 1 time
  Then the state of the land grant should be finished
  When I advance the land grant 1 time
  Then the error "Land grant finished" should occur

Scenario: Land grant plot selection
  Given I create a default map
  And I finish map creation
  And I create the following players:
    | name     | type    |
    | A        | Flapper |
    | B        | Packer  |
  And I create a land grant with the current map and players
  When I start the land grant
  And player A selects the plot
  Then the current plot should contain the following attributes:
    | x | y | type   | state  | owner  |
    | 1 | 1 |        | taken  | A      |
  When I advance the land grant 22 times
  And player A selects the plot
  Then the current plot should contain the following attributes:
    | x | y | type  | state  | owner  |
    | 5 | 3 | store | taken  | system |
  When I advance the land grant 1 time
  And player A selects the plot
  Then the current plot should contain the following attributes:
    | x | y | type  | state  | owner  |
    | 6 | 3 |       | free   |        |
  When player B selects the plot
  Then the current plot should contain the following attributes:
    | x | y | type  | state  | owner  |
    | 6 | 3 |       | taken  | B      |