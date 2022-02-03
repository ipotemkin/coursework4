"""This module contains a flask app"""

from flask import Flask, render_template, request, redirect
from typing import Union

from app.classes import UnitClass
from app.equipment import Equipment
from app.unit import HumanPlayer, CompPlayer
from app.arena import Arena

app = Flask("__main__")
app.config["JSON_AS_ASCII"] = False
equipment = Equipment()
ARENA = Arena()


def prepare_form_data(header: str):
    return {
        "header": header,
        "classes": UnitClass.get_unit_names(),
        "weapons": equipment.get_weapon_names(),
        "armors": equipment.get_armor_names()
    }


def render_fighting_screen(func: Union[str, callable]):
    return render_template(
        "fight.html",
        heroes={"player": ARENA.hero, "enemy": ARENA.enemy},
        result=(func() if ARENA.game_on else "Бой окончен!") if type(func) != str else func
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/choose-hero/", methods=["GET"])
def choose_hero():
    if ARENA.game_on:
        return "Вы опоздали, игра уже идет!"
    ARENA.game_on = True
    return render_template("hero_choosing.html", result=prepare_form_data("Выберите героя"))


@app.route("/choose-hero/", methods=["POST"])
def choose_hero_post():
    hero_type = UnitClass.get_unit_by_name(request.form["unit_class"])
    hero = HumanPlayer(
        name=request.form["name"],
        unit_class=hero_type,
        health=hero_type.max_health,
        stamina=hero_type.max_stamina,
        _weapon=equipment.get_weapon(request.form["weapon"]),
        _armor=equipment.get_armor(request.form["armor"]),
    )
    ARENA.hero = hero
    return redirect('/choose-enemy/')


@app.route("/choose-enemy/", methods=["GET"])
def choose_enemy():
    return render_template("hero_choosing.html", result=prepare_form_data("Выберите противника"))


@app.route("/choose-enemy/", methods=["POST"])
def choose_enemy_post():
    hero_type = UnitClass.get_unit_by_name(request.form["unit_class"])
    hero = CompPlayer(
        name=request.form["name"],
        unit_class=hero_type,
        health=hero_type.max_health,
        stamina=hero_type.max_stamina,
        _weapon=equipment.get_weapon(request.form["weapon"]),
        _armor=equipment.get_armor(request.form["armor"]),
    )
    ARENA.enemy = hero
    return redirect("/fight/")


@app.route("/fight/")
def fight():
    return render_fighting_screen("Бой начался!")


@app.route("/fight/hit")
def fight_hit():
    return render_fighting_screen(ARENA.attack)


@app.route("/fight/use-skill")
def fight_use_skill():
    return render_fighting_screen(ARENA.use_skill)


@app.route("/fight/pass-turn")
def fight_pass_turn():
    return render_fighting_screen(ARENA.skip_turn)


@app.route("/fight/end-fight")
def fight_end_fight():
    ARENA.game_on = False
    return render_fighting_screen("Бой окончен!")


if __name__ == "__main__":
    app.run()
