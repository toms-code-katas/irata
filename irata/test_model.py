from irata.model import Map, Player, ResourceState
from unittest import TestCase


class TestPlayer(TestCase):

    def test_calculate_energy_units_needed(self):
        resource = "energy"
        player = Player(name="test-1", player_type="Flapper", money=100)
        energy = ResourceState(name=resource)
        player.resource_states[resource] = energy

        self.assertEquals(1, player.calculate_units_needed(resource, Map()))

    def test_calculate_energy_spoilage(self):
        resource = "energy"
        player = Player(name="test-1", player_type="Flapper", money=100)
        energy = ResourceState(name=resource)
        player.resource_states[resource] = energy

        self.assertEquals(0, player.calculate_spoilage(resource), "Spoilage should be 0 if no units are left "
                                                                  "from the previous turn")

        energy.previous_amount = 10
        self.assertEquals(5, player.calculate_spoilage(resource), "Spoilage should be half of the units left "
                                                                  "from the previous turn")
