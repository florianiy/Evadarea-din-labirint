from collections import deque
from pprint import pprint


def find_positions(maze):

    exits = getExits(maze)

    print(exits)

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


# Example maze and exits
maze = [[]]


def maze_to_matrix(maze_string):
    maze_rows = maze_string.splitlines()
    maze_matrix = [list(row) for row in maze_rows]
    return maze_matrix


filename = f"./labirinturi/{str(1)}.txt"
with open(filename) as f:
    text = f.read()
    maze = maze_to_matrix(text)


def getMaze(id):
    filename = f"./labirinturi/{str(id)}.txt"
    with open(filename) as f:
        return f.read()


exits = [(3, 0), (9, 6), (6, 9)]
positions = find_positions(maze_to_matrix(getMaze(1)))
print(positions)
