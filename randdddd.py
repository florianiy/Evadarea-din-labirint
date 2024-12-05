import random
from collections import deque


def find_exits(maze):
    exits = []
    size = len(maze)

    # Top and bottom rows
    for col in range(size):
        if maze[0][col] == 0:  # Top row
            exits.append((0, col))
        if maze[size - 1][col] == 0:  # Bottom row
            exits.append((size - 1, col))

    # Left and right columns (excluding corners already added)
    for row in range(1, size - 1):
        if maze[row][0] == 0:  # Left column
            exits.append((row, 0))
        if maze[row][size - 1] == 0:  # Right column
            exits.append((row, size - 1))

    return exits


def place_player_and_monster(maze):
    exits = find_exits(maze)

    size = len(maze)

    # bfs to all recheable positions
    def bfs_distance(start):
        distances = [[-1] * size for _ in range(size)]
        queue = deque([start])
        distances[start[0]][start[1]] = 0

        while queue:
            x, y = queue.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < size
                    and 0 <= ny < size
                    and maze[nx][ny] == 0
                    and distances[nx][ny] == -1
                ):
                    distances[nx][ny] = distances[x][y] + 1
                    queue.append((nx, ny))
        return distances

    def is_valid_player_position(x, y):
        if maze[x][y] != " ":
            return False
        distances = bfs_distance((x, y))
        return all(
            distances[ex[0]][ex[1]] >= 3
            for ex in exits
            if distances[ex[0]][ex[1]] != -1
        )

    # 3 manhattan distance away
    def get_monster_positions(player_x, player_y):
        positions = []
        for dx in range(-3, 4):
            dy = 3 - abs(dx)
            for sign in [-1, 1]:
                nx, ny = player_x + dx, player_y + sign * dy
                if 0 <= nx < size and 0 <= ny < size and maze[nx][ny] == 0:
                    positions.append((nx, ny))
        return positions

    # find all player pos
    valid_player_positions = [
        (x, y)
        for x in range(size)
        for y in range(size)
        if is_valid_player_position(x, y)
    ]
    if not valid_player_positions:
        raise ValueError("No valid positions for the player found.")

    # try find monster until you have no more player pos
    random.shuffle(valid_player_positions)
    for player_x, player_y in valid_player_positions:
        monster_positions = get_monster_positions(player_x, player_y)
        if monster_positions:
            monster_x, monster_y = random.choice(monster_positions)
            maze[player_x][player_y] = "P"
            maze[monster_x][monster_y] = "M"
            return maze, (player_x, player_y), (monster_x, monster_y)

    raise ValueError(
        "Could not place both player and monster under the given conditions."
    )
