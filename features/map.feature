Feature: Creation of maps based on various parameters like store location or river plots

Scenario: Default map creation
  When I create a default map
  And I finish map creation
  Then the maps size should be 9 x 5
  And the map contains the following plots:
    | x  | y | type  |
    | 5  | 1 | river |
    | 5  | 2 | river |
    | 5  | 3 | store |
    | 5  | 4 | river |
    | 5  | 5 | river |

Scenario: Customized map creation
  Given I create a customized map
  And the maps size is 10 x 3
  And I finish map creation
  And the map contains the following plots:
    | x  | y | type  |
    | 1  | 1 | store |
    | 2  | 1 | river |
    | 2  | 2 | river |
    | 2  | 3 | river |
  Then the maps size should be 10 x 3
  And the map should contain the following plots:
    | x  | y | type  |
    | 1  | 1 | store |
    | 2  | 1 | river |
    | 2  | 2 | river |
    | 2  | 3 | river |
  And plots of type mountain should be randomly distributed

Scenario: Customized map creation without mandatory store
  When I create a customized map
  Then the maps size is 9 x 5
  And I finish map creation
  Then the error "No store location given" should occur