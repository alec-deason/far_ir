from far_ir import DescribedObject, Exit, game_loop

def main():
    player = DescribedObject(["self"], "It's you")

    foyer = DescribedObject(["foyer"], "It's a foyer.")
    inner_room = DescribedObject(["inner room"], "It's a room.")

    f_to_i = Exit(["west"], inner_room)
    foyer.children.add(f_to_i)
    i_to_f = Exit(["east"], foyer)
    inner_room.children.add(i_to_f)

    table = DescribedObject(["table"], "It's a table", "There is a table here")
    coat_rack = DescribedObject(["coat rack", "rack"], "It's a coat rack", "There is a coat rack here")
    player.parent = foyer
    table.parent = foyer
    foyer.children.add(player)
    foyer.children.add(table)
    inner_room.children.add(coat_rack)

    game_loop(player)

if __name__ == "__main__":
    main()

