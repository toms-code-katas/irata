from behave import step, use_step_matcher

use_step_matcher("re")


@step('I create a (default|customized) map')
def create_a_map(context, map_type):
    """
    :type context: behave.runner.Context
    :param map_type: The type of the map
    """
    print(map_type)
    # raise NotImplementedError(f'STEP: Given I create a {map_type} map')
    pass


@step('the maps size is (\\d+) x (\\d+)')
def map_size_is(context, x: int, y: int):
    """
    :param y: The y size
    :param x: The x size
    :type context: behave.runner.Context
    """
    # raise NotImplementedError(f'STEP: the maps size is {x} x {y}')
    pass

@step('the store is located at (\\d+),(\\d+)')
def store_is_located_at(context, x: int, y: int):
    """
    :param y: The y size
    :param x: The x size
    :type context: behave.runner.Context
    """
    # raise NotImplementedError(f'STEP: the store is located at {x} x {y}')
    pass
