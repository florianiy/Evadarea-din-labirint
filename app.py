from json import dumps
from random import randrange
from flask import Flask, json, render_template, request


app = Flask(__name__)

player_pos = []
monster = ()
maze = [[]]
move_counter = 0

ROAD = " "
WALL = "#"
MONSTER = "M"
MAZE_SIZE = 10
MAZE_COUNT = 5


def maze_to_matrix(maze_string):
    maze_rows = maze_string.splitlines()
    maze_matrix = [list(row) for row in maze_rows]
    return maze_matrix


def get_random_maze():
    global MAZE_COUNT
    # nr = randrange(1, MAZE_COUNT + 1)
    nr = 1
    filename = f"./labirinturi/{str(nr)}.txt"
    with open(filename) as f:
        text = f.read()
        global maze
        maze = maze_to_matrix(text)


def generate_player():
    global player_pos
    player_pos = [1, 2]


def generate_monster():
    global monster
    monster = (1, 3)


def move_player(dir):

    global player_pos
    new_pos = player_pos.copy()
    if dir == "U":
        new_pos[1] -= 1
    if dir == "D":
        new_pos[1] += 1
    if dir == "L":
        new_pos[0] -= 1
    if dir == "R":
        new_pos[0] += 1
    return new_pos


def get_char_at(pos):
    global maze
    return maze[pos[0]][pos[1]]


def hit_exit(pos):
    row = pos[1]
    col = pos[0]
    is_on_edge = row == 0 or row == MAZE_SIZE - 1 or col == 0 or col == MAZE_SIZE - 1
    return is_on_edge and get_char_at(pos) == ROAD


def hit_monster(pos):
    global monster
    return pos == list(monster)


def hit_wall(pos):
    return get_char_at(pos) == WALL


def game_won():
    global move_counter
    return f"""
Ai reușit!
Ai ieșit din labirint în {move_counter} mișcări
"""


def game_over():
    return """Ai
picat pradă monstrului din labirint … ai pierdut jocul. Încerca din nou!"""


@app.route("/")
def index():
    return render_template("game.html")


@app.route("/start")
def start_game():
    global move_counter
    move_counter = 0
    get_random_maze()
    generate_player()
    generate_monster()
    global player_pos
    return dumps(player_pos)


@app.route("/move")
def move():
    direction = request.args.get("direction")
    new_pos = move_player(direction)
    result = {"data": new_pos.copy()}
    if hit_exit(new_pos):
        result["msg"] = game_won()
        result["action"] = "WON"
    elif hit_monster(new_pos):
        result["msg"] = game_over()
        result["action"] = "LOST"
    elif hit_wall(new_pos):
        result["msg"] = "Imposibil, ai lovit un perete. Încearcă altă directie."
        result["action"] = "WALL"
    else:
        #  actual move
        global move_counter
        move_counter += 1
        global player_pos
        player_pos = new_pos.copy()
        result["msg"] = "OK"
        result["action"] = "OK"
    return dumps(result)


@app.route("/get_player_pos")
def get_player_pos():
    global player_pos
    return dumps(player_pos)


if __name__ == "__main__":
    app.run(debug=True)
