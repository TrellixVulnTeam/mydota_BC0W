from django.shortcuts import render, redirect
import dota2api
from django.http import HttpResponse
import pprint
import json
import jsbeautifier
from json2html import *
import os
from datetime import timedelta

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


def player_summary_view(request, account_id):

    query = request.GET.get("q")
    if query:
        return redirect('main:match_detail', match_id = query)

    player_history = api.get_match_history(account_id=account_id, matches_requested=2)
    player_history = player_history["matches"]
    heroes = api.get_heroes()
    heroes = heroes["heroes"]
    player_sum = api.get_player_summaries(steamids=76561198086198097)
    kills_list = []
    deaths_list = []
    assists_list = []

    for current_match in player_history:
        match = api.get_match_details(match_id=current_match["match_id"])
        current_match["duration"] = match["duration"]
        current_match["duration"] = timedelta(seconds=current_match["duration"])


        # Handling player picture
        def player_pic():
            global x
            x=0
            while x<10:
                if int(current_match["players"][x]["account_id"]) == int(account_id):
                    for hero in heroes:
                        if hero["id"] == current_match["players"][x]['hero_id']:
                            return hero["url_large_portrait"]
                x+=1
        current_match["player_pic"] = player_pic()

        current_match["player_kills"] = match["players"][x]["kills"]
        kills_list.append(current_match["player_kills"])

        current_match["player_deaths"] = match["players"][x]["deaths"]
        deaths_list.append(int(current_match["player_deaths"]))

        current_match["player_assists"] = match["players"][x]["assists"]
        assists_list.append(int(current_match["player_assists"]))

        current_match["game_mode_name"] = match["game_mode_name"]

        # Handling Result win/loss
        # rad_win=0
        # rad_member=0
        # if match["radiant_win"] == True:
        #     rad_win = 1
        # else:
        #     rad_win = 0
        # i=0
        # while i<5:
        #     if match["players"][i]["account_id"] == str(account_id):
        #         rad_member= 1
        #         i=5
        #     i+=1
        # print(rad_member)
        # print(rad_win)
        # current_match["victory"] = rad_win+rad_member
        # if rad_member + rad_win in (2, 0):
        #     current_match["victory"] = "Won match"
        # else:
        #     current_match["victory"] = "Lost match"

    context={
        "player_history" : player_history,
        "player_sum": player_sum,
        "kills_list" : kills_list,
        "deaths_list" : deaths_list,
        "assists_list" : assists_list,
    }

    return render(request, "player_summary.html", context)

def search_view(request, search_id):


    if api.get_match_details(match_id=search_id):
        print('helo')
    else:
        api.get_match_history(account_id=search_id, matches_requested=1)
        print('íyello')
    return HttpResponse("hu")
    # match_id = query
    # player_history = api.get_match_history(account_id=account_id, matches_requested=2)
    # player_history = player_history["matches"]
    # match = api.get_match_details(match_id=match_id)
    # match_ = json2html.convert(json=match)



def match_detail_view(request, match_id=None):

    query = request.GET.get("q")
    if query:
        return redirect('main:search_view', search_id=query)

    items = api.get_game_items()
    items_ = json2html.convert(json=items)

    heroes = api.get_heroes()
    heroes_ = json2html.convert(json=heroes)

    match = api.get_match_details(match_id=match_id)
    match_ = json2html.convert(json=match)

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
    match["duration"] = timedelta(seconds=match["duration"])

    # Retrieving avatars
    for player in players:
        player["stead_id"] = player["account_id"] + 76561197960265728
        player_sum = api.get_player_summaries(steamids=player["stead_id"])
        player["name"] = player_sum["players"][0]["personaname"]
        player["prof_pic"] = player_sum["players"][0]["avatarmedium"]


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


