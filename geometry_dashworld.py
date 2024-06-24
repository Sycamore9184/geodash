from entities import player, spike, post
from datetime import datetime
from colorama import Back, init
import utils
import os

init(autoreset=True)


class Game:
    def __init__(
        self,
        configuration: dict = {
            "debug": True,
            "dimensions": {"width": 120, "height": 50},
        },
    ):
        self.game_state = {
            "over": False,
            "entities": 0,
            "died_to": 0,  # Entity ID
            # Can add more states here, such as total score, etc.
        }
        self.debug = configuration["debug"]
        self.dimensions = configuration["dimensions"]
        self.entities = {
            "player": player,
            "spike": spike,
            "post": post,
        }
        self.world = {
            "map": [],
            "entities": [],
        }

    def get_entity_count(self):
        return len(self.world["entities"])

    # Return the player entity
    # The player entity is always the first entity in the list
    def get_player(self):
        return self.world["entities"][0]

    # Return the entity with the given ID
    # If the entity is not found, return a default entity
    def get_entity(self, entity_id: int):
        entity = filter(lambda x: x["id"] == entity_id, self.world["entities"])

        return next(entity, {"id": -1, "name": "none"})

    def log(self, message: str):
        if self.debug:
            print(f"[{datetime.now()}] [DEBUG] {message}", flush=True)

    # Generate the world map, player, spikes, and posts.
    # Entities are generated in pairs (as per requirement), and placed randomly on the map
    def create_world(self):
        self.world["map"] = [
            ["5" for _ in range(self.dimensions["width"])]
            for _ in range(self.dimensions["height"])
        ]

        self.generate_player()

        for _ in range(2):
            self.generate_enemy()
            self.generate_post()

    # Generate a player entity and append it to the entity list
    def generate_player(self):
        player = self.entities["player"].copy()
        # Stick to the ground
        player["y"] = self.dimensions["height"] - 7
        player["id"] = self.get_entity_count()

        self.world["entities"].append(player)

    # Generate an enemy entity and append it to the entity list
    def generate_enemy(self):
        new_spike = utils.generate_entity_position(
            post.copy(),
            self.world["entities"],
            self.dimensions["width"],
            self.dimensions["height"],
        )

        new_spike["id"] = self.get_entity_count()

        self.world["entities"].append(new_spike)

    # Generate a post entity and append it to the entity list
    def generate_post(self):
        new_post = utils.generate_entity_position(
            spike.copy(),
            self.world["entities"],
            self.dimensions["width"],
            self.dimensions["height"],
        )

        new_post["id"] = self.get_entity_count()

        self.world["entities"].append(new_post)

    # Overwrite the world map with the body of the entity at the given coordinates
    def render_entity(self, x: int, y: int, body: list[str]):
        for i in range(len(body)):
            for j in range(len(body[i])):
                if (
                    # Check if the entity is within the bounds of the world
                    y - i < self.dimensions["height"]
                    and x + j < self.dimensions["width"]
                    # Ignore the entity background tiles
                    and body[i][j] != "4"
                ):
                    self.world["map"][y - i][x + j] = body[i][j]

    # Call render_entity for each entity in the entity list
    def render_entities(self):
        for entity in self.world["entities"]:
            self.render_entity(entity["x"], entity["y"], entity["body"])

    # Render the world map
    def draw_world(self):
        map = self.world["map"]

        # Clear the console if not in debug mode
        # This is done to simulate a real-time game
        # If in debug mode, the console will not be cleared so that the logs can be seen
        if not self.debug:
            os.system("clear" if os.name == "posix" else "cls")

        # Overwrite the last 6 rows of the world with the floor tiles
        for x in range(len(map[:-6])):
            for y in range(len(map[x])):
                map[x][y] = "4"

        # Overwrite the world tiles with each entity at their respective coordinates
        # This must be done before the actual rendering takes place
        self.render_entities()

        for x in range(len(map)):
            row = ""

            # Assign colors to each tile
            for y in range(len(map[x])):
                if map[x][y] == "0":
                    row += Back.BLACK + " "
                elif map[x][y] == "1":
                    row += Back.LIGHTGREEN_EX + " "
                elif map[x][y] == "2":
                    row += Back.LIGHTBLUE_EX + " "
                elif map[x][y] == "3":
                    row += Back.YELLOW + " "
                elif map[x][y] == "4":
                    row += Back.LIGHTWHITE_EX + " "
                elif map[x][y] == "5":
                    row += Back.WHITE + " "

            # Actual rendering
            print(row, flush=True)

        if not self.debug:
            return

        for entity in self.world["entities"]:
            self.log(
                f"Rendered entity [{entity['id']}:{entity['name']}] at ({entity['x']}, {entity['y']}).\tbounds: {utils.calculate_entity_bounds(entity)}"
            )

        self.log(f"Entity count: {self.get_entity_count()}")

        if self.game_state["over"]:
            entity = self.get_entity(self.game_state["died_to"])

            self.log(f"Game over! You died to [{entity['id']}:{entity['name']}]")

    # Move the player entity based on the user input
    # This function also checks for collisions with the enemy entities
    # If a collision is detected, the game is over
    def move_player(self, option):
        userinput = option.split(" ")
        player = self.get_player()

        # Since we're calling .split(" ") on the input, we can have multiple inputs
        # separated by a space. This allows for multiple key presses in one frame
        for i in range(len(userinput)):
            key = userinput[i]

            if key == "left" or key == "a" and player["x"] > 1:
                player["x"] -= 16
            elif (
                key == "right"
                or key == "d"
                and player["x"] < self.dimensions["width"] - 30
            ):
                player["x"] += 16
            # Jumping is a bit more complex, if we later on decide to render each frame
            # we might have to change this logic, along with the rendering logic
            elif key == "up" or key == "w" and player["y"] > 30:
                player["y"] -= 17
                player["x"] += 32
                player["y"] += 17

        # Check for collisions with enemy entities
        for entity in self.world["entities"]:
            if not entity["type"] == "enemy":
                continue

            has_collided = utils.determine_collision(player, entity)

            if has_collided:
                self.game_state["over"] = True
                self.game_state["died_to"] = entity["id"]
                break

        # Determine if the game is over after every move
        # Theres probably a better way to do this
        return self.game_state["over"]
