import geometry_dashworld as game


def main():
    game.create_world()

    while True:
        game.draw_world()

        GAME_OVER = game.move_player(input())

        if GAME_OVER:
            game.draw_world()
            break


if __name__ == "__main__":
    main()
