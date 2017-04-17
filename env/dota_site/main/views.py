from django.shortcuts import render, redirect
import dota2api
from django.http import HttpResponse
import pprint
import json
import jsbeautifier
from json2html import *
import os
from datetime import timedelta
from jchart import Chart
from jchart.config import Title, Axes

api = dota2api.Initialise()
matches_requested = 10


def dec_to_bin(x):
    return int(bin(x)[2:])


def load_json_file(file_name):
    inp_file = os.path.abspath(os.path.join(os.path.dirname
    (os.path.abspath(__file__)), "..", "static",file_name))
    return inp_file



def main_view(request):

    query = request.GET.get("match_id")

    if query:
        return redirect('main:search_view', search_id = query)
    else:
        return render(request, 'main.html')



def search_view(request, search_id):

    try:
        match = api.get_match_details(match_id=search_id)
        
        heroes = api.get_heroes()
        heroes_ = json2html.convert(json=heroes)
        heroes = heroes["heroes"]
        players = match['players']
        for player in players:
            for hero in heroes:
                if player["hero_id"] == hero["id"]:
                    player["hero_img_url"] = hero["url_large_portrait"]

        if match["radiant_win"] == True:
            match['victory'] = "Radiant Victory"
        else:
            match['victory'] = "Dire Victory"

        context={
            "match" : match,
            "players" : players,
        }
        return render(request, "search_view.html", context)
    except:

        player = api.get_match_history(
            account_id=search_id,
            matches_requested=matches_requested)

        context={
            "player" : player,
        }
        return render(request, "search_view.html", context)




def player_summary_view(request, account_id):
    


    query = request.GET.get("q")
    if query:
        return redirect('main:match_detail', match_id = query)

    player_history = api.get_match_history(account_id=account_id, matches_requested=matches_requested)
    player_history = player_history["matches"]
    heroes = api.get_heroes()
    heroes = heroes["heroes"]
    player_sum = api.get_player_summaries(steamids=76561198086198097)
    kills_list = []
    deaths_list = []
    assists_list = []
    GPM_list = []
    XPM_list = []


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
        kills_list.append(int(current_match["player_kills"]))

        current_match["player_deaths"] = match["players"][x]["deaths"]
        deaths_list.append(int(current_match["player_deaths"]))

        current_match["player_assists"] = match["players"][x]["assists"]
        assists_list.append(int(current_match["player_assists"]))

        GPM_list.append(match["players"][x]["gold_per_min"])
        XPM_list.append(match["players"][x]["xp_per_min"])

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

    class KDA(Chart):
        chart_type = 'line'
        title = Title(text='KDA over the past 25 games')
        scales = {
            'xAxes': [
            Axes(position='bottom', scaleLabel= 
                {
                'display':'true', 'labelString':"Latest-->Most recent"
                }
                )
            ],
        }


        def get_datasets(self, **kwargs):
            return [{
                'label' : "Kills",
                'data' : kills_list,
                'backgroundColor' : [
                'rgba(75, 192, 192, 0.2)',
            ],
                'borderColor': [
                'rgba(75, 192, 192, 1)',
            ],
            'borderWidth' : 1,
            },{
                'label' : "Deaths",
                'data' : deaths_list,
                'backgroundColor' : [
                'rgba(255, 99, 132, 0.2)'],
                'borderColor': [
                'rgba(255, 99, 132, 1)'],
                'borderWidth' : 1,
            },{
                'label' : "Assists",
                'data' : assists_list,
                'backgroundColor' : [
                'rgba(255, 206, 86, 0.2)'],
                'borderColor': [
                'rgba(255, 206, 86, 1)'],
                'borderWidth' : 1,
            }]

        def get_labels(self, **kwargs):
            return list(range(1, matches_requested+1))


    class GPM_XPM(Chart):
        chart_type = 'line'
        scales = {
            'xAxes': [
            Axes(position='bottom', scaleLabel= 
                {
                'display':'true', 'labelString':"Latest-->Most recent"
                }
                )
            ],
        }


        def get_datasets(self, **kwargs):
            return [{
                'label' : "GPM",
                'data' : GPM_list,
                'backgroundColor' : [
                'rgba(75, 192, 192, 0.2)',
            ],
                'borderColor': [
                'rgba(75, 192, 192, 1)',
            ],
            'borderWidth' : 1,
            },{
                'label' : "XPM",
                'data' : XPM_list,
                'backgroundColor' : [
                'rgba(255, 99, 132, 0.2)'],
                'borderColor': [
                'rgba(255, 99, 132, 1)'],
                'borderWidth' : 1,
            }]

        def get_labels(self, **kwargs):
            return list(range(1, matches_requested+1))

    context={
        "player_history" : player_history,
        "player_sum": player_sum,
        "KDA" : KDA(),
        "GPM_XPM" : GPM_XPM(),
    }

    return render(request, "player_summary.html", context)






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
        try:
            player["name"] = player_sum["players"][0]['personaname']
            player["prof_pic"] = player_sum["players"][0]["avatarmedium"]
        except:
            player["name"] = "Anonymous"
            player["prof_pic"] = ""
            player["account_id"] = ""
        
    

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


