from behave import step, use_step_matcher
from irata.model import Map

use_step_matcher("re")


@step('I create a (default|customized) map')
def create_a_map(context, map_type):
    """
    :type context: behave.runner.Context
    :param map_type: The type of the map
    """
    if map_type == "default":
        mapp = Map()
        mapp.create()
        context.map = mapp
    else:
        raise NotImplementedError(f'STEP: I create a (default|customized) map')


@step('I finish map creation')
def finish_map_creation(context):
    """
    :type context: behave.runner.Context
    """
    assert context.map is not None


@step('the maps size (is|should be) (\\d+) x (\\d+)')
def map_size_is(context, is_or_should: str, x: int, y: int):
    """
    :param y: The y size
    :param x: The x size
    :param is_or_should: Whether the size is or should be
    :type context: behave.runner.Context
    """
    assert context.map.width == int(x)
    assert context.map.height == int(y)
    assert len(context.map.get_plots()) == int(x) * int(y)


@step('the store (is|should be) located at (\\d+),(\\d+)')
def store_is_located_at(context, is_or_should: str, x: int, y: int):
    """
    :param is_or_should: Whether the store is or should be located
    :param y: The y size
    :param x: The x size
    :type context: behave.runner.Context
    """
    # raise NotImplementedError(f'STEP: the store is located at {x} x {y}')
    pass


@step('the map contains the following plots')
def map_contains_plots(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step('plots of type (mountain|river) are randomly distributed')
def map_contains_plots(context, plot_type: str):
    """
    :param plot_type: The type of the plot
    :type context: behave.runner.Context
    """
    pass


@step('the error "(.*)" should occur')
def error_should_occur(context, error: str):
    """
    :param error: The error
    :type context: behave.runner.Context
    """
    pass


