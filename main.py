from geometry_dashworld import Game


def main():
    game = Game(
        {
            "debug": True,
            "dimensions": {"width": 120, "height": 50},
        }
    )

    game.create_world()

    while True:
        game.draw_world()
        game.move_player(input())

        if game.is_over():
            game.draw_world()
            break


if __name__ == "__main__":
    main()
