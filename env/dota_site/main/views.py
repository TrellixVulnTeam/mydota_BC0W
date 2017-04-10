from django.shortcuts import render, redirect
import dota2api
from django.http import HttpResponse
import pprint
import json
import jsbeautifier
from json2html import *
import os

api = dota2api.Initialise()

def dec_to_bin(x):
    return int(bin(x)[2:])

def load_json_file(file_name):
    inp_file = os.path.abspath(os.path.join(os.path.dirname
    (os.path.abspath(__file__)), "..", "static",file_name))
    return inp_file


def main_view(request):

    query = request.GET.get("match_id")

    if query:
        return redirect('main:match_detail', match_id = query)
    else:
        return render(request, 'main.html')


def match_detail_view(request, match_id=None):


    query = request.GET.get("q")
    if query:
        match_id = query
    match = api.get_match_details(match_id=match_id)




    match_ = json2html.convert(json=match)

    items = api.get_game_items()
    items_ = json2html.convert(json=items)

    heroes = api.get_heroes()
    heroes_ = json2html.convert(json=heroes)

    with open(load_json_file("abilities.json")) as abilities_json:
        abilities = json.load(abilities_json)
    abilities = abilities["abilities"]



    if match["radiant_win"] == True:
        victory = "Radiant Victory"
    else:
        victory = "Dire Victory"
    
    players = match['players']
    heroes = heroes["heroes"]
    rad_heroes = players[0:5]
    dire_heroes = players[5:10]
    builds_col_num = range(1, 26)

    # Handling item and hero image URLs

    # Ability URLS
    def get_item_url(id):
        for ability in abilities:
            if ability['id'] == str(id):
                return ability['name']

    for player in players:
        for upgrade in player['ability_upgrades']:
            ability_name = get_item_url(upgrade['ability'])
            if ability_name == None:
                upgrade['ability_url'] ="../static/spellicons/talent_tree.jpg"
            else:
                upgrade['ability_url'] = "http://cdn.dota2.com/apps/dota2/images/abilities/%s_lg.png" % ability_name

    # Item URLS
    for player in players:
        i = 0
        while i<6:
            current_item = player["item_%d" % i]
            if current_item == 0:
                player["item_%d_url_img" % i] = "/static/items/emptyitembg.png"
            else:
                for item in items["items"]:
                    if item["id"] == current_item:
                        player["item_%d_url_img" % i] = item["url_image"]
            i += 1

    # Backpack URLS
    for player in players:
        i = 0
        while i<3:
            current_backpack = player["backpack_%d" % i]
            if current_backpack == 0:
                player["backpack_%d_url_img" % i] = "/static/items/emptyitembg.png"
            else:
                for item in items["items"]:
                    if item["id"] == current_backpack:
                        player["backpack_%d_url_img" % i] = item["url_image"]
            i += 1

    # Hero URLS
    for player in players:
        for hero in heroes:
            if player["hero_id"] == hero["id"]:
                player["hero_img_url"] = hero["url_large_portrait"]

    context={
        "match_" : match_,
        "match" : match,
        "victory" : victory,
        "rad_heroes" : rad_heroes,
        "dire_heroes" : dire_heroes,
        "players" : players,
        "items_" : items_,
        "heroes_" : heroes_,
        "builds_col_num" : builds_col_num,
    }

    return render(request, 'match_detail.html', context)


