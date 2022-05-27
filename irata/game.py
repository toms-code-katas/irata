import time

from model import LandGrant, LandGrantState, Map

land_grant: LandGrant = None

mmap = Map()
mmap.create()
land_grant = LandGrant(mapp=mmap)

if __name__ == "__main__":
    print("Starting land grant")
    land_grant.start()
    while land_grant.state == LandGrantState.ONGOING:
        print(
            f"Land grant currently at plot: {land_grant.get_current_plot().coordinates.x}, "
            f"{land_grant.get_current_plot().coordinates.y}")
        time.sleep(0.1)
        land_grant.advance()
