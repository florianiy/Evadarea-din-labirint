from collections import deque


from collections import deque
from json import dumps
from pprint import pprint


def getExits(m):
    rows, cols = len(m), len(m[0])
    e = []

    # Check all four edges of the m
    for i in range(rows):
        if m[i][0] == " ":  # Left edge
            e.append((i, 0))
        if m[i][cols - 1] == " ":  # Right edge
            e.append((i, cols - 1))

    for j in range(cols):
        if m[0][j] == " ":  # Top edge
            e.append((0, j))
        if m[rows - 1][j] == " ":  # Bottom edge
            e.append((rows - 1, j))

    return e


def get_possible_player_positions(maze):

    exits = getExits(maze)

    rows, cols = len(maze), len(maze[0])
    distances = [[-1] * cols for _ in range(rows)]
    queue = deque()

    # Initialize BFS with all exits
    for exit in exits:
        x, y = exit
        queue.append((x, y, 0))
        distances[x][y] = 0

    # BFS to calculate distances
    while queue:
        x, y, dist = queue.popleft()

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < rows
                and 0 <= ny < cols
                and maze[nx][ny] == " "
                and distances[nx][ny] == -1
            ):
                distances[nx][ny] = dist + 1
                queue.append((nx, ny, dist + 1))

    result = [(i, j) for i in range(rows) for j in range(cols) if distances[i][j] >= 3]
    return result


def maze_to_matrix(maze_string):
    maze_rows = maze_string.splitlines()
    maze_matrix = [list(row) for row in maze_rows]
    return maze_matrix


def getMaze(id):
    filename = f"./labirinturi/{str(id)}.txt"
    with open(filename) as f:
        return f.read()


def is_reachable(maze, start, exits):
    rows, cols = len(maze), len(maze[0])
    visited = [[False] * cols for _ in range(rows)]
    queue = deque([start])

    while queue:
        x, y = queue.popleft()
        if (x, y) in exits:
            return True  # Found an exit

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < rows
                and 0 <= ny < cols
                and maze[nx][ny] == " "
                and not visited[nx][ny]
            ):
                visited[nx][ny] = True
                queue.append((nx, ny))

    return False  # No path to any exit


def get_monster_positions(player_pos, maze):
    px, py = player_pos
    rows, cols = len(maze), len(maze[0])
    potential_positions = []

    # Find all positions exactly 3 Manhattan distance away
    for dx in range(-3, 4):
        dy = 3 - abs(dx)
        for nx, ny in [(px + dx, py + dy), (px + dx, py - dy)]:
            if (
                0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == " "
            ):  # Must be within bounds and open
                potential_positions.append((nx, ny))

    return potential_positions


def find_valid_monster_positions(maze, players, exits):
    result = []

    for player_pos in players:
        px, py = player_pos
        monster_positions = []

        # Get potential monster positions for this player
        for mx, my in get_monster_positions(player_pos, maze):
            # Temporarily block the position with a monster
            maze[mx][my] = "#"
            all_reachable = all(is_reachable(maze, player, exits) for player in players)
            maze[mx][my] = " "  # Restore the maze

            if all_reachable:
                monster_positions.append([mx, my])

        if monster_positions:
            result.append([[px, py], monster_positions])

    return result


def precompute_maze_player_monster_locations(maze_nr):
    maze = maze_to_matrix(getMaze(maze_nr))
    exits = getExits(maze)
    positions = get_possible_player_positions(maze)
    result = find_valid_monster_positions(maze, positions, exits)
    path = f"./labirinturi/{maze_nr}.json"
    with open(path, "w") as file:
        file.write(dumps(result))
    return result


# print(precompute_maze_player_monster_locations(1))
