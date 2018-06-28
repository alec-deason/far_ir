from far_ir.fluent_interface import Game

def main():
    ctx = Game()

    ctx.p.description("It's you").noun("self")
    ctx.o("glass").description("It's an empty glass").can_pickup(True)
    ctx.o("key").description("It's a key").can_pickup(True)
    ctx.o("table").description("It's a table")
    ctx.o("coat_rack").description("It's a coat rack").noun("coat rack")

    ctx.r("foyer").description("It's a foyer").contains(ctx.p, "table", "glass", "key").exit("west", "inner_room", "key")
    ctx.r("inner_room").description("It's a room").noun("room").contains("coat_rack").exit("east", "foyer")

    ctx.run()


if __name__ == "__main__":
    main()
