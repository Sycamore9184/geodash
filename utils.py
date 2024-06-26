import random

random.seed()


def calculate_entity_bounds(entity):
    width = len(entity["body"][0]) // 2
    height = len(entity["body"]) // 2

    left = entity["x"] - width
    right = entity["x"] + width
    top = entity["y"] + height
    bottom = entity["y"] - height

    return left, right, top, bottom


def determine_collision(entity1, entity2):
    left1, right1, top1, bottom1 = calculate_entity_bounds(entity1)
    left2, right2, top2, bottom2 = calculate_entity_bounds(entity2)

    x_collision = not (right1 < left2 or right2 < left1)
    y_collision = not (top1 < bottom2 or top2 < bottom1)

    return x_collision and y_collision


def is_too_close(new_entity, existing_entities, min_distance):
    for entity in existing_entities:
        if determine_collision(new_entity, entity):
            print(
                f"Entity {new_entity['name']}(x: {new_entity['x']}, y: {new_entity['y']}) is colliding with {entity['name']}(x: {entity['x']}, y: {entity['y']})",
                flush=True,
            )

            return True

        dx = new_entity["x"] - entity["x"]
        dy = new_entity["y"] - entity["y"]

        distance = ((dx) ** 2 + (dy) ** 2) ** 0.5

        if distance < min_distance:
            print(
                f"Entity {new_entity['name']}(x: {new_entity['x']}, y: {new_entity['y']}) is too close to {entity['name']}(x: {entity['x']}, y: {entity['y']})",
                flush=True,
            )
            return True

    return False


def generate_entity_position(
    new_entity, existing_entities, world_width, world_height, min_distance=15
):
    while True:
        new_entity["x"] = random.randint(min_distance, world_width - min_distance)
        new_entity["y"] = world_height - 7

        print(
            f"Trying to place entity {new_entity['name']} at ({new_entity['x']}, {new_entity['y']})",
            flush=True,
        )

        if not is_too_close(new_entity, existing_entities, min_distance):
            return new_entity
