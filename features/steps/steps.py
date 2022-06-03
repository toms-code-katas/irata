from behave import step, use_step_matcher
from irata.model import Map, PlotType, Plot, LandGrant, Player, PlayerType, ResourceState

use_step_matcher("re")


@step('I create a (default|customized) map')
def create_a_map(context, map_type):
    """
    :type context: behave.runner.Context
    :param map_type: The type of the map
    """
    mapp = Map()
    context.map = mapp


@step('I create a land grant with the current map(| and players)')
def create_a_land_grant(context, with_players:str):
    """
    :type context: behave.runner.Context
    :param with_players: players should be included in the land grant
    """
    land_grant = LandGrant(mapp=context.map)
    if with_players:
        land_grant.players = context.players

    context.land_grant = land_grant


@step('I start the land grant')
def create_a_land_grant(context):
    """
    :type context: behave.runner.Context
    """
    context.land_grant.start()


@step('I finish map creation')
def finish_map_creation(context):
    """
    :type context: behave.runner.Context
    """
    assert context.map is not None
    mapp = context.map
    try:
        mapp.create()
    except Exception as e:
        context.exception = e


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
def map_contains_plots(context, contains_or_should_contain):
    """
    :param contains_or_should_contain: Should or contains
    :type context: behave.runner.Context
    """
    mapp = context.map
    for row in context.table:
        x = int(row["x"])
        y = int(row["y"])
        plot_type = (row["type"])
        plot = mapp.get_plot_at(x, y)
        if contains_or_should_contain == "should contain":
            assert plot
            assert plot.plot_type.value == plot_type
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
    exception: Exception = context.exception
    assert exception
    assert str(exception) == error


@step('the state of the land grant should be (ongoing|finished)')
def state_of_land_grant_should_be(context, expected_state: str):
    """
    :param expected_state: The expected state
    :type context: behave.runner.Context
    """
    land_grant_state = context.land_grant.state.value
    assert land_grant_state == expected_state


@step('the current plot should contain the following attributes')
def state_of_current_plot(context):
    plot: Plot = context.land_grant.get_current_plot()
    for row in context.table:
        x = int(row["x"])
        y = int(row["y"])
        plot_type = row["type"]
        state = row["state"]
        owner = row["owner"]
        assert plot.coordinates.x == x
        assert plot.coordinates.y == y
        if plot_type:
            assert plot.plot_type.value == plot_type
        if state:
            assert plot.state.value == state
        if owner:
            assert plot.owner == owner


@step('I advance the land grant (\\d+) times*?')
def advance_land_grant(context, times: str):
    for i in range(0, int(times)):
        try:
            context.land_grant.advance()
        except Exception as e:
            context.exception = e


@step('I create the following players')
def create_players(context):
    context.players = {}
    for row in context.table:
        name = row["name"]
        player_type = row["type"]
        context.players[name] = Player(name=name, player_type=PlayerType(player_type))


@step('player (\\w+) selects the plot')
def player_selects_plot(context, player_name):
    context.land_grant.select_current_plot(context.players[player_name])


@step('the players have the following state for (food|energy|smithore|crystite)')
def player_state_for_resource(context, resource: str):
    for row in context.table:
        player = context.players[row["name"]]
        resource_state = ResourceState(resource)
        resource_state.previous_amount = int(row["previous amount"])
        if "usage" in row.headings:
            resource_state.usage = int(row["usage"])
        if "production" in row.headings:
            resource_state.production = int(row["production"])
        player.resource_states[resource] = resource_state


@step('I calculate the spoilage of (food|energy|smithore|crystite) for player (\\w+)')
def calculate_spoilage(context, resource: str, player: str):
    player = context.players[player]
    player.calculate_spoilage(resource)


@step('I calculate the spoilage of (food|energy|smithore|crystite) for all players')
def calculate_spoilage_for_all_players(context, resource: str):
    for player in context.players:
        calculate_spoilage(context, resource, player)


@step('player (\\w+) should have spoiled (\\d+) unit(?:s)? of (food|energy|smithore|crystite)')
def player_should_have_spoiled(context, player: str, units: str, resource: str):
    player = context.players[player]
    assert player.resource_states[resource].spoilage == int(units)


@step('I calculate the surplus / shortage of (food|energy) for all players')
def calculate_surplus_for_all_players(context, resource: str):
    mapp = None
    try:
        mapp = context.map
    except AttributeError:
        pass
    for player in context.players.values():
        player.calculate_surplus(resource, player.calculate_units_needed(resource, mapp))


@step("player (\\w+) should have a (shortage|surplus) of (\\d+) unit(?:s)? of (food|energy)")
def player_should_have_surplus(context, player: str, shortage_or_surplus: str, units: str, resource: str):
    player = context.players[player]
    actual_surplus = player.resource_states[resource].surplus
    expected_surplus = int(units)
    if shortage_or_surplus == "shortage":
        assert actual_surplus == -expected_surplus
    else:
        assert actual_surplus == expected_surplus


@step("the players own the following plots")
def players_own_plots(context):

    for row in context.table:
        player = context.players[row["name"]]
        x = int(row["x"])
        y = int(row["y"])
        mapp = context.map
        plot = mapp.get_plot_at(x, y)
        plot.owner = player.name
