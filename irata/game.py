from random import randint
import threading
import time

from model import LandGrant, LandGrantState, Map, Player, PlayerType

land_grant: LandGrant = None
players = {}

mmap = Map()
players["A"] = Player(name="A", player_type=PlayerType(name="Flapper"))
mmap.create()
land_grant = LandGrant(mapp=mmap, players=players)


def simulate_player_a():
    global land_grant
    global players
    while land_grant.state == LandGrantState.ONGOING:
        time.sleep(randint(1, 5))
        if not land_grant.state == LandGrantState.ONGOING:
            return
        if land_grant.select_current_plot(players["A"]):
            print(f"Selected plot {land_grant.get_current_plot().coordinates.x},"
                  f" {land_grant.get_current_plot().coordinates.y}")
        else:
            print(f"Could not select plot {land_grant.get_current_plot().coordinates.x},"
                  f" {land_grant.get_current_plot().coordinates.y}")


if __name__ == "__main__":
    print("Starting land grant")
    land_grant.start()
    player_a_thread = threading.Thread(target=simulate_player_a)
    player_a_thread.daemon = True
    player_a_thread.start()
    while land_grant.state == LandGrantState.ONGOING:
        print(
            f"Land grant currently at plot: {land_grant.get_current_plot().coordinates.x}, "
            f"{land_grant.get_current_plot().coordinates.y}")
        time.sleep(1)
        land_grant.advance()
    player_a_thread.join(timeout=0)
