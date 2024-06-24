from geometry_dashworld import Game


def main():
    game = Game(
        configuration={
            "debug": True,
            "dimensions": {"width": 120, "height": 50},
        }
    )

    game.create_world()

    while True:
        game.draw_world()

        GAME_OVER = game.move_player(input())

        if GAME_OVER:
            game.draw_world()
            break


if __name__ == "__main__":
    main()
