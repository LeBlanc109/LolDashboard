#So this file SHOULD have relative path set, so add the imports up here
import json
import requests
import pandas as pd

def first_function(api_key):
    #RIOT API KEY: 
    auth = api_key

    #Step 1 -> READ the JSON (we could call it similarily to the rank one, but to save on api calls for now)
    with open("match_timeline.json", "r") as file:
        data = json.load(file)

    lane_template = {
        1: "top", 2: "jungle", 3: "mid", 4: "bot", 5: "supp",
        6: "top", 7: "jungle", 8: "mid", 9: "bot", 10: "supp"
    }
    
    team_template = {
        1: 100, 2: 100, 3: 100, 4: 100, 5: 100,  # Blue buff/team
        6: 200, 7: 200, 8: 200, 9: 200, 10: 200   # Red buff/ team
    }

    #A. Puuid -> gameName + tagLines
    player_gamertags = {}
    
    for participant_id, player_unique in enumerate(data["metadata"]["participants"], start=1):
        response = requests.get(
            f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{player_unique}?api_key={auth}'
        )

        player_data = response.json()
        player_gamertags[participant_id] = f"{player_data['gameName']}#{player_data['tagLine']}"

    rows_data = []
    for frame_idx, frame in enumerate(data["info"]["frames"]):
        for participant_id, participant_stats in frame["participantFrames"].items():
            statz = participant_stats

            #Arguably most importanyl we need the FRAME
            statz['frame'] = frame_idx

            #Step 2 -> CLEAN the DATA, 
            #first POP
            statz.update(statz.pop('championStats'))
            statz.update(statz.pop('damageStats'))
            statz.update(statz.pop('position'))

            #clean the values we want right now to numbers... (theyre strings in pbi)
            statz['totalGold'] = int(statz.get('totalGold' , 0))
            statz["level"] = int(statz.get('level' , 0))

            #something
            statz['player_gamertag'] = player_gamertags[int(participant_id)]
            statz['position'] = lane_template[int(participant_id)]
            statz['team'] = team_template[int(participant_id)]

            #Step 3 -> this one requires transforming AND cleaning in 1
            statz['creep_score'] = int(statz.get('minionsKilled' , 0) + statz.get('jungleMinionsKilled' , 0))
            
            rows_data.append(statz)

    lastgame_df = pd.DataFrame(rows_data)
    lastgame_df['PBISource'] = 'Last Game'


    return lastgame_df