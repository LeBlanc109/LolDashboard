#So this file SHOULD have relative path set, so add the imports up here
import json
import requests
import pandas as pd

def first_function(api_key):
    #RIOT API KEY: 
    auth = api_key

    #Step 1 -> READ the JSON
    with open("match_timeline.json", "r") as file:
        data = json.load(file)

        #A. The PUUIDs are at the top of the match.json, use to get gameName + tagLine
    player_gamertags = {}

    for item in data["info"]["participants"]:
        participant_id = item["participantId"]
        puuid = item["puuid"]
        response = requests.get(
            f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={auth}'
        )

        player_data = response.json()
        player_gamertags[participant_id] = f"{player_data['gameName']}#{player_data['tagLine']}"

    rows_data = []
    for frame_idx, frame in enumerate(data["info"]["frames"]):
        for participant_id, participant_stats in frame["participantFrames"].items():

            #Arguably most importanyl we need the FRAME
            participant_stats['frame'] = frame_idx

            #Step 2 -> CLEAN the DATA
            participant_stats.update(participant_stats.pop('championStats'))
            participant_stats.update(participant_stats.pop('damageStats'))
            participant_stats.update(participant_stats.pop('position'))

            #Step 3 -> TRANSFORM the DATA
            participant_stats['creep_score'] = participant_stats.get('minionsKilled') + participant_stats.get('jungleMinionsKilled')

            participant_stats['player_gamertag'] = player_gamertags[int(participant_id)]
            rows_data.append(participant_stats)

    df = pd.DataFrame(rows_data)
    return df