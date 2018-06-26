from far_ir import DescribedObject, Exit, game_loop
from far_ir.linguistics import Thing, Container

def main():
    player = DescribedObject(Thing("self"), "It's you", visible=False)

    foyer = DescribedObject(Container("foyer", preposition="in"), "It's a foyer.")
    inner_room = DescribedObject(Container("room", preposition="in"), "It's a room.")

    f_to_i = Exit("west", inner_room)
    foyer.children.add(f_to_i)
    i_to_f = Exit("east", foyer)
    inner_room.children.add(i_to_f)

    table = DescribedObject(Container("table"), "It's a table")
    chair = DescribedObject(Container("chair"), "It's a chair")
    coat_rack = DescribedObject(Thing("coat rack"), "It's a coat rack")
    player.parent = foyer
    table.parent = foyer
    chair.parent = foyer
    foyer.children.add(player)
    foyer.children.add(table)
    foyer.children.add(chair)
    inner_room.children.add(coat_rack)

    game_loop(player)

if __name__ == "__main__":
    main()

