from entities import player, spike, post
from colorama import Back, init
import utils
import os

init(autoreset=True)

DEBUG = True
GAME_OVER = False
WORLD_WIDTH = 120
WORLD_HEIGHT = 50

player["x"] = 1
player["y"] = WORLD_HEIGHT - 7

world = {}


# Crear una funci ́on create wold( ) que cree la matriz que contenga el mundo de tama ̃no 50 x 120 celdas de espacio.
def create_world():
    global world

    world = {
        "map": [["5" for _ in range(WORLD_WIDTH)] for _ in range(WORLD_HEIGHT)],
        "entities": [player.copy()],
    }

    # Add entities to the world
    # Note that this will generate entities, but they will not be rendered
    #
    # TODO: Move entity generation to a separate function
    for _ in range(1):
        new_post = utils.generate_entity_position(
            spike.copy(), world["entities"], WORLD_WIDTH, WORLD_HEIGHT
        )
        world["entities"].append(new_post)

        new_spike = utils.generate_entity_position(
            post.copy(), world["entities"], WORLD_WIDTH, WORLD_HEIGHT
        )

        world["entities"].append(new_spike)


# Crear una funci ́on draw player( ) que permita dibujar el cuadrado (jugador) en la posici ́on como se muestra en la Figura 1
# Esta función se ha reemplazado por render_entity, ya que el jugador es una entidad más
def render_entity(x: int, y: int, entity: list[str]):
    global world

    for i in range(len(entity)):
        for j in range(len(entity[i])):
            if (
                y - i >= 0
                and y - i < WORLD_HEIGHT
                and x + j >= 0
                and x + j < WORLD_WIDTH
            ):
                # Overwrite the world map with the entity
                world["map"][y - i][x + j] = entity[i][j]


# Crear una funci ́on draw world( ) que permita dibujar todo el mundo
def draw_world():
    global world

    # Reference to avoid writing world["map"] every time
    map = world["map"]

    if not DEBUG:
        # Clear the console every frame
        os.system("clear" if os.name == "posix" else "cls")

    # Render the floor
    for i in range(len(map[:-6])):
        for j in range(len(map[i])):
            map[i][j] = "4"

    render_entities()

    for i in range(len(map)):
        row = ""
        # Assign colors to the pixels of the world
        # otherwise the console will show numbers
        #
        # TODO: use a different library that allows transparency
        for j in range(len(map[i])):
            if map[i][j] == "0":
                row += Back.BLACK + " "
            elif map[i][j] == "1":
                row += Back.LIGHTGREEN_EX + " "
            elif map[i][j] == "2":
                row += Back.LIGHTBLUE_EX + " "
            elif map[i][j] == "3":
                row += Back.YELLOW + " "
            elif map[i][j] == "4":
                row += Back.LIGHTWHITE_EX + " "
            elif map[i][j] == "5":
                row += Back.WHITE + " "

        print(row, flush=True)

    # Debug information, useful to know if the entities are being generated correctly
    if DEBUG:
        for entity in world["entities"]:
            print(
                f"[DEBUG] Rendered entity [{entity['name']}] at ({entity['x']}, {entity['y']})",
                flush=True,
            )
        print(f"[DEBUG] Entity count: {len(world['entities'])}", flush=True)

        if GAME_OVER:
            print(
                f"[DEBUG] Entity {world['entities'][0]['name']} touched a spike. Game over",
                flush=True,
            )


def render_entities():
    for i in range(0, len(world["entities"])):
        entity = world["entities"][i]

        render_entity(entity["x"], entity["y"], entity["body"])

        print(
            f"[DEBUG] {entity['name']} bounds: {utils.calculate_entity_bounds(entity)}",
            flush=True,
        )


# Crear una funci ́on move player(option) que permita mover un conjunto celdas de la
# posici ́on del jugador. En el caso de cuadrado cada movimiento horizontal(right) son
# 16 celdas, en caso sea un movimiento arriba (up) son 17 celdas hacia arriba, luego 32
# celdas a la derecha y finalmente 16 celdas hacia abajo, el objetivo es que de un saldo.
def move_player(option):
    global GAME_OVER

    userinput = option.split(" ")
    player = world["entities"][0]

    for i in range(len(userinput)):
        key = userinput[i]

        # TODO: these 'and' checks might be removed for the final version
        if key == "left" or key == "a" and player["x"] > 1:
            player["x"] -= 16
        elif key == "right" or key == "d" and player["x"] < WORLD_WIDTH - 30:
            player["x"] += 16
        elif key == "up" or key == "w" and player["y"] > 30:
            player["y"] -= 17
            player["x"] += 32
            player["y"] += 17
        # elif key == "s" and player["y"] < 43:
        #    player["y"] += 17

    for i in range(1, len(world["entities"])):
        entity = world["entities"][i]
        has_collided = utils.determine_collision(player, entity)

        if entity["type"] == "enemy" and has_collided:
            GAME_OVER = True
            break

    return GAME_OVER
