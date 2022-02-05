"""This module contains a flask app"""

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.wrappers.response import Response
from typing import Union, Callable

from app.classes import UnitClass
from app.equipment import Equipment
from app.unit import HumanPlayer, CompPlayer
from app.arena import Arena

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.url_map.strict_slashes = False
app.config["ARENA"] = Arena()  # to store the arena
app.config["EQUIPMENT"] = Equipment()  # to store the equipment


def prepare_form_data(header: str) -> dict:
    """
    to prepare data for a player form to fulfil
    """

    return {
        "header": header,
        "classes": UnitClass.get_unit_names(),
        "weapons": app.config["EQUIPMENT"].get_weapon_names(),
        "armors": app.config["EQUIPMENT"].get_armor_names(),
    }


def render_fighting_screen(func: Union[str, Callable]) -> Union[str, Response]:
    """
    renders the fighting screen depending from the args
    """

    if (
        app.config["ARENA"].hero == NotImplemented
        or app.config["ARENA"].enemy == NotImplemented
    ):
        return redirect(url_for("index"))
    return render_template(
        "fight.html",
        heroes={"player": app.config["ARENA"].hero, "enemy": app.config["ARENA"].enemy},
        result=(func() if app.config["ARENA"].is_game_on() else "Бой окончен!")
        if type(func) != str
        else func,
    )


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/choose-hero/", methods=["GET"])
def choose_hero() -> Union[str, Response]:
    if app.config["ARENA"].is_game_on():
        return render_template("ongoing.html")
    app.config["ARENA"].start_game()
    return render_template(
        "hero_choosing.html", result=prepare_form_data("Выберите героя")
    )


@app.route("/choose-hero/", methods=["POST"])
def choose_hero_post() -> Response:
    hero_type = UnitClass.get_unit_by_name(request.form["unit_class"])
    app.config["ARENA"].hero = HumanPlayer(
        name=request.form["name"],
        unit_class=hero_type,
        health=hero_type.max_health,
        stamina=hero_type.max_stamina,
        _weapon=app.config["EQUIPMENT"].get_weapon(request.form["weapon"]),
        _armor=app.config["EQUIPMENT"].get_armor(request.form["armor"]),
    )
    return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy/", methods=["GET"])
def choose_enemy() -> Union[str, Response]:
    if app.config["ARENA"].hero == NotImplemented:
        return redirect(url_for("index"))
    return render_template(
        "hero_choosing.html", result=prepare_form_data("Выберите противника")
    )


@app.route("/choose-enemy/", methods=["POST"])
def choose_enemy_post() -> Response:
    hero_type = UnitClass.get_unit_by_name(request.form["unit_class"])
    app.config["ARENA"].enemy = CompPlayer(
        name=request.form["name"],
        unit_class=hero_type,
        health=hero_type.max_health,
        stamina=hero_type.max_stamina,
        _weapon=app.config["EQUIPMENT"].get_weapon(request.form["weapon"]),
        _armor=app.config["EQUIPMENT"].get_armor(request.form["armor"]),
    )
    return redirect(url_for("fight"))


@app.route("/fight/")
def fight() -> Union[str, Response]:
    return render_fighting_screen("Бой начался!")


@app.route("/fight/hit")
def fight_hit() -> Union[str, Response]:
    return render_fighting_screen(app.config["ARENA"].attack)


@app.route("/fight/use-skill")
def fight_use_skill() -> Union[str, Response]:
    return render_fighting_screen(app.config["ARENA"].use_skill)


@app.route("/fight/pass-turn")
def fight_pass_turn() -> Union[str, Response]:
    return render_fighting_screen(app.config["ARENA"].skip_turn)


@app.route("/fight/end-fight")
def fight_end_fight() -> Response:
    app.config["ARENA"].end_game()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
