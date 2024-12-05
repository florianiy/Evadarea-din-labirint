import copy
from json import dumps
from random import randrange
from flask import Flask, json, render_template, request
import random
from collections import deque


app = Flask(__name__)

player_pos = []
monster_pos = ()
maze = [[]]
move_counter = 0
precomputed_id = ""

ROAD = " "
WALL = "#"
MONSTER = "M"
MAZE_SIZE = 10
MAZE_COUNT = 5


def maze_to_matrix(maze_string):
    maze_rows = maze_string.splitlines()
    maze_matrix = [list(row) for row in maze_rows]
    return maze_matrix


# 1<=exits<=3
def get_random_maze(nr=-1):
    global MAZE_COUNT
    if nr == -1:
        nr = randrange(1, MAZE_COUNT + 1)
    filename = f"./labirinturi/{str(nr)}.txt"
    with open(filename) as f:
        text = f.read()
        global maze
        maze = maze_to_matrix(text)


def generate_player_and_monster(maze_nr):
    filename = f"./labirinturi/{str(maze_nr)}.json"
    with open(filename) as f:
        mlist = json.loads(f.read())
        random_player_pos = random.randint(0, len(mlist) - 1)
        monsters = mlist[random_player_pos]
        global player_pos, monster_pos
        player_pos = monsters[0]
        random_monster = random.randint(0, len(monsters[1]) - 1)
        monster_pos = monsters[1][random_monster]
        global precomputed_id
        precomputed_id = f"seed:{maze_nr}:{random_player_pos}:{random_monster}"


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
    return maze[pos[1]][pos[0]]


def hit_exit(pos):
    row = pos[1]
    col = pos[0]
    is_on_edge = row == 0 or row == MAZE_SIZE - 1 or col == 0 or col == MAZE_SIZE - 1
    return is_on_edge and get_char_at(pos) == ROAD


def hit_monster(pos):
    global monster_pos
    return pos == list(monster_pos)


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
    get_random_maze(1)
    generate_player_and_monster(1)
    global player_pos
    return dumps(player_pos)


@app.route("/get_precomputed_id")
def get_precomputed_id():
    global precomputed_id
    return precomputed_id


@app.route("/move")
def move():
    direction = request.args.get("direction")
    new_pos = move_player(direction)
    result = {"data": new_pos.copy()}
    global move_counter
    if hit_exit(new_pos):
        move_counter += 1
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
