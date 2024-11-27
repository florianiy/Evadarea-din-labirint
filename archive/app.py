from random import randrange
from flask import Flask, json, render_template, request


app = Flask(__name__)

MAZE_COUNT = 5
CURR_MAZE = [[]]
player = ()


@app.route("/")
def index():
    return render_template("game.html")


@app.route("/builder")
def maze_builder():
    return render_template("maze-builder.html")


@app.route("/random-maze")
def get_random_maze():
    rand_maze = randrange(1, MAZE_COUNT + 1)
    filename = f"./labirinturi/{str(rand_maze)}.txt"
    with open(filename) as f:
        maze = f.read()
        global CURR_MAZE
        CURR_MAZE = maze_to_matrix(maze)
        print(maze)
        global player
        player = (randrange(3, 7 + 1), randrange(3, 7 + 1))
        while CURR_MAZE[player[0]][player[1]] == "#":
            player = (randrange(3, 7 + 1), randrange(3, 7 + 1))
        return ("?" * 10 + "\n") * 10


def start_game():
    get_random_maze()
    player_pos = generate_player_position()
    generate_monster_position()
    return player_pos


def get_move(asd):
    return "#"


@app.route("/move")
def move():
    direction = request.args.get("direction")
    next_pos = get_move(direction)
    if next_pos == "#":
        return "wall"
    if next_pos == "M":
        return "game over"
    # if(next_pos == " " and is(next_pos))


@app.route("/get-player-pos")
def get_player_pos():
    return json.dumps(player)


def maze_to_matrix(maze_string):
    maze_rows = maze_string.splitlines()
    maze_matrix = [list(row) for row in maze_rows]
    return maze_matrix


if __name__ == "__main__":
    app.run(debug=True)
