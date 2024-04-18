import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display_html

NHLData = pd.read_csv("/content/NHLStandings.csv")

Teams = {"Atlantic" : ["Florida Panthers", "Boston Bruins", "Toronto Maple Leafs",
            "Tampa Bay Lightning", "Detroit Red Wings", "Buffalo Sabres",
            "Ottawa Senators", 	"Montreal Canadiens"],

        "Central" : ["Dallas Stars", "Winnipeg Jets", "Colorado Avalanche",
                    "Nashville Predators", "St. Louis Blues", "Minnesota Wild",
                "Arizona Coyotes", "Chicago Blackhawks"],

        "Metropolitan" : ["New York Rangers", "Carolina Hurricanes", "New York Islanders",
                    "Washington Capitals", "Pittsburgh Penguins", "Philadelphia Flyers",
                    "New Jersey Devils", "Columbus Blue Jackets"],

        "Pacific" : ["Vancouver Canucks", "Edmonton Oilers", "Vegas Golden Knights",
                    "Los Angeles Kings", "Calgary Flames", 	"Seattle Kraken",
                    "Anaheim Ducks", "San Jose Sharks"]}

def get_division(team):
    return list(filter(lambda x: team in Teams[x], Teams))[0]

splits = []
for i in range(len(NHLData)):
    splits.append( list(map(int, NHLData["Overall"][i].split("-"))))
    ot_wins = int(NHLData["Overtime"][i].split("-")[0]) + int(NHLData["Shootout"][i].split("-")[0])
    splits[-1].append(int(splits[-1][0]) - ot_wins)
    splits[-1].append(ot_wins)

my_data = pd.DataFrame(splits, columns = ["W", "RL", "OTL", "RW", "OTW"])

my_data["Team"] = NHLData["Team"]
my_data = my_data[["Team", "RW", "OTW", "RL", "OTL"]]

my_data["Pts"] = 2*(my_data["RW"] + my_data["OTW"]) + my_data["OTL"]
my_data["NewPts"] = 3*my_data["RW"] + 2*my_data["OTW"] + my_data["OTL"]
my_data["Division"] = [get_division( my_data["Team"][i] ) for i in range(len(my_data)) ]

Point_types = ["Pts", "NewPts"]

def get_division_standings(Division, Points = "Pts", Playoffs = True):

    division_data = my_data.loc[my_data["Division"] == Division].sort_values(
        by = [Points, "RW"], ascending = False).reset_index(drop=True)
    division_data.index += 1
    if Playoffs:
        return division_data.drop(columns = ["Division", Point_types[(Point_types.index(Points)+1)%2 ]])[0:4]
    return division_data.drop(columns = ["Division", Point_types[(Point_types.index(Points)+1)%2 ]])

def get_conference_standings(Conference, Points = "Pts", Playoffs = True):
    East, West = ["Atlantic", "Metropolitan"], ["Central", "Pacific"]
    if Conference == "East":
        conference_data = my_data.loc[my_data["Division"].isin(East)].sort_values(
            by = [Points, "RW"], ascending = False).reset_index(drop=True)
        conference_data.index += 1
        if Playoffs:
            return conference_data.drop(columns = [Point_types[(Point_types.index(Points)+1)%2 ]])[0:8]
        return conference_data.drop(columns = [Point_types[(Point_types.index(Points)+1)%2 ]])

    conference_data = my_data.loc[my_data["Division"].isin(West)].sort_values(
        by = [Points, "RW"], ascending = False).reset_index(drop=True)
    conference_data.index += 1
    if Playoffs:
        return conference_data.drop(columns = [Point_types[(Point_types.index(Points)+1)%2 ]])[0:8]
    return conference_data.drop(columns = [Point_types[(Point_types.index(Points)+1)%2 ]])

def compare_tables(df1, df2):
    df1_styler = df1.style.set_table_attributes("style='display:inline'").set_caption('Current Points System')
    df2_styler = df2.style.set_table_attributes("style='display:inline'").set_caption('Proposed Points System')

    display_html(df1_styler._repr_html_()+df2_styler._repr_html_(), raw=True)

def compare_conference(Conference):
    df1 = get_conference_standings(Conference)
    df2 = get_conference_standings(Conference, Points = "NewPts")
    return compare_tables(df1, df2)

def compare_division(Division):
    df1 = get_division_standings(Division)
    df2 = get_division_standings(Division, Points = "NewPts")
    return compare_tables(df1, df2)
