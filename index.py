from flask import Flask, redirect, url_for, render_template, request
from main import *
import json
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def home_post():
    width = request.form['width']
    height = request.form['height']
    danger = request.form['danger']
    weapon = request.form['weapon']
    heal = request.form['heal']
    return redirect(url_for("createGame", dimensions = ','.join([width, height, danger, weapon, heal])))

@app.route('/createGame/<dimensions>')
def createGame(dimensions = None):
    w, h, d, we, hea = dimensions.split(',')
    return render_template("create_game.html", width = w, height = h, danger = d, weapon = we, heal = hea)

@app.route('/createGame/<dimensions>', methods=["POST"])
def create_post(dimensions = None):
    w, h, d, we, hea = dimensions.split(',')
    num_players = int(request.form['player_count'])
    try:
        stats = ["height", "strength", "speed", "intelligence", "creativity"]
        players = {}
        for i in range(1, num_players+1):
            name = request.form[f"{i}-name"]
            players[f"{name}"] = {
                x: float(request.form[f"{i}-{x}"]) for x in stats
                
            }
        return redirect(url_for("playGame", dimensions = dimensions, players = json.dumps(players)))
    except:
        return render_template("create_game_player_selection.html", num_players=int(num_players), width = w, height = h, danger = d, weapon = we, heal = hea)

@app.route('/playGame/<dimensions>/<players>')
def playGame(dimensions = None, players = None):
    w, h, d, we, hea = dimensions.split(',')
    print
    return HungerGames_web(int(we), int(d), int(w), int(h), int(hea), json.loads(players))

if __name__ == '__main__':
    app.run()
