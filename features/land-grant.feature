Feature: Land grants let players choose a plot from the map

Scenario: Land grant general process
  Given I create a customized map
  And the maps size is 3 x 3
  And the store is located at 2,2
  And I finish map creation
  When I start the land grant
  Then the state of the land grant should be "ongoing"
  Then the current plot should contain the following attributes:
    | x | y | type  | state | owner |
    | 1 | 1 | land  | free  |       |
  When I advance the land grant 4 times
  Then the current plot should contain the following attributes:
    | x | y | type  | state | owner |
    | 5 | 1 | river | free  |       |
  When I advance the land grant 19 times
  Then the current plot should contain the following attributes:
    | x | y | type  | state  | owner  |
    | 5 | 3 | store | taken  | system |
  When I advance the land grant 22 times
  Then the current plot should contain the following attributes:
    | x | y | type  | state  | owner  |
    | 9 | 5 | land  | free   |        |
  When I advance the land grant 1 time
  Then the state of the land grant should be "finished"
  When I advance the land grant 1 time
  Then the error "Land grant finished" should occur