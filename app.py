"""This module contains a flask app"""

from flask import Flask, render_template, request, jsonify, redirect

from app.classes import UnitClass
from app.equipment import Equipment
from app.skills import ConcreteSkill
from app.unit import HumanPlayer, CompPlayer
from app.arena import Arena

app = Flask("__main__")
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["JSON_AS_ASCII"] = False
equipment = Equipment()
HEROES = dict()
ARENA = Arena()


def prepare_data_for_form(header: str):
    return {
        "header": header,
        "classes": UnitClass.get_unit_names(),
        "weapons": equipment.get_weapon_names(),
        "armors": equipment.get_armor_names()
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/choose-hero/", methods=["GET"])
def choose_hero():
    return render_template("hero_choosing.html", result=prepare_data_for_form("Выберите героя"))


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
    # global HEROES
    # HEROES["player"] = hero
    # print(hero)
    ARENA.hero = hero
    return redirect('/choose-enemy/')


@app.route("/choose-enemy/", methods=["GET"])
def choose_enemy():
    return render_template("hero_choosing.html", result=prepare_data_for_form("Выберите противника"))


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
    # global HEROES
    # HEROES["enemy"] = hero
    # print(hero)
    ARENA.enemy = hero
    # return "Enemy set up"
    return redirect("/fight/")


@app.route("/fight/")
def fight():
    # print(HEROES)
    return render_template(
        "fight.html",
        heroes={"player": ARENA.hero, "enemy": ARENA.enemy},
        # result="Result name",
        result="Бой начался!"
    )


@app.route("/fight/hit")
def fight_hit():
    # global HEROES
    # battle_result = HEROES["player"].attack(HEROES["enemy"])
    # battle_result += ". " + HEROES["enemy"].attack(HEROES["player"])
    # print(battle_result)
    # return render_template("fight.html", heroes=HEROES, result="Result name 1", battle_result=battle_result)
    battle_result = ARENA.hero.attack(ARENA.enemy)
    battle_result += ".\n" + ARENA.enemy.attack_or_use_skill(ARENA.hero)
    ARENA.regenerate_stamina()
    print(battle_result)
    return render_template(
        "fight.html",
        heroes={"player": ARENA.hero, "enemy": ARENA.enemy},
        # result="Result name",
        result=battle_result
    )


if __name__ == "__main__":
    app.run()
