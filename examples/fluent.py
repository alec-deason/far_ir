from far_ir.fluent_interface import Game

def main():
    ctx = Game()

    ctx.p.description("It's you").noun("self")
    ctx.o("glass").description("It's an empty glass")
    ctx.o("table").description("It's a table").contains("glass")
    ctx.o("coat_rack").description("It's a coat rack").noun("coat rack")

    ctx.r("foyer").description("It's a foyer").contains(ctx.p, "table").exit("west", "inner_room")
    ctx.r("inner_room").description("It's a room").noun("room").contains("coat_rack").exit("east", "foyer")

    ctx.run()


if __name__ == "__main__":
    main()
