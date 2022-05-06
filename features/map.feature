Feature: Creation of maps based on various parameters like store location or river plots

Scenario: Default map creation
  When I create a default map
  Then the maps size should be 9 x 5
  And the store should be located at 4,3
  And plots of type "river" should be located at:
    | x  | y |
    | 5  | 1 |
    | 5  | 2 |
    | 5  | 4 |
    | 5  | 5 |

Scenario: Customized map creation
  When I start creating a customized map
  Then the maps size is 10 x 3
  And the store is located at 1,1
  And plots of type "river" are located at:
    | x  | y |
    | 2  | 1 |
    | 2  | 2 |
    | 2  | 3 |
  And plots of type "mountain" are randomly distributed
  And I finish map creation
  Then the maps size should be 10 x 3
  And the store should be located at 1,1
  And plots of type "river" should be located at:
    | x  | y |
    | 2  | 1 |
    | 2  | 2 |
    | 2  | 3 |

Scenario: Customized map creation without mandatory store
  When I start creating a customized map
  Then the maps size is 9 x 5
  And I finish map creation
  Then the error "No store location given" should occur