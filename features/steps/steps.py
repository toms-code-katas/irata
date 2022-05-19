from behave import step, use_step_matcher
from irata.model import Map, PlotType

use_step_matcher("re")


@step('I create a (default|customized) map')
def create_a_map(context, map_type):
    """
    :type context: behave.runner.Context
    :param map_type: The type of the map
    """
    mapp = Map()
    context.map = mapp


@step('I finish map creation')
def finish_map_creation(context):
    """
    :type context: behave.runner.Context
    """
    assert context.map is not None
    mapp = context.map
    mapp.create()


@step('the maps size (is|should be) (\\d+) x (\\d+)')
def map_size_is(context, is_or_should: str, x: int, y: int):
    """
    :param y: The y size
    :param x: The x size
    :param is_or_should: Whether the size is or should be
    :type context: behave.runner.Context
    """
    mapp = context.map
    if is_or_should == "is":
        mapp.width = int(x)
        mapp.height = int(y)
    elif is_or_should == "should be":
        assert mapp.width == int(x)
        assert mapp.height == int(y)
        assert len(context.map.get_plots()) == int(x) * int(y)


@step('the map (contains|should contain) the following plots')
def map_contains_plots(context, contains_or_shoud_contain):
    """
    :type context: behave.runner.Context
    """
    mapp = context.map
    for row in context.table:
        x = int(row["x"])
        y = int(row["y"])
        plot_type = (row["type"])
        plot = mapp.get_plot_at(x, y)
        if contains_or_shoud_contain == "should contain":
            assert plot
            assert str(plot.plot_type) == plot_type
        else:
            plot.plot_type = PlotType(plot_type)


@step('plots of type (mountain|river) should be randomly distributed')
def randomly_distributed_plots(context, plot_type: str):
    """
    :param plot_type: The type of the plot
    :type context: behave.runner.Context
    """
    mountains = 0
    for plot in context.map.get_plots():
        if plot.plot_type == PlotType.MOUNTAIN:
            mountains += 1

    assert mountains > 0

@step('the error "(.*)" should occur')
def error_should_occur(context, error: str):
    """
    :param error: The error
    :type context: behave.runner.Context
    """
    pass


