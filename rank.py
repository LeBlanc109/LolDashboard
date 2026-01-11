import pandas as pd
import requests
import json
import os

#os.chdir(r'COPY OATH TO THE PROJECT FOLDER')

#RIOT AUTH + 
auth = ''
#TBD I'm SILVER, but other people aren't so... we'll have to be able to configure that for later
#requested_rank = ''

def get_ladder_rung(division):
    return requests.get(
        f'https://na1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/SILVER/{division}?page=1&api_key={auth}'
    ).json()

def get_timeline(ladder_json, player_index=15):
    puuid = ladder_json[player_index].get('puuid')
    match_id = requests.get(
        f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=1&api_key={auth}'
    ).json()[0]
    return requests.get(
        f'https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline?api_key={auth}'
    ).json()

def fill_rank_tl(timeline_data):
    rows_data = []
    for frame_idx, frame in enumerate(timeline_data["info"]["frames"]):
        for participant_id, stats in frame["participantFrames"].items():
            stats['frame'] = frame_idx
            stats['participantId'] = int(participant_id)
            
            # popping the stats dicts
            stats.update(stats.pop('championStats'))
            stats.update(stats.pop('damageStats'))
            stats.update(stats.pop('position'))
            
            # need creep_score because jungle minions have a seperate variable
            stats['creep_score'] = stats.get('minionsKilled', 0) + stats.get('jungleMinionsKilled', 0)
            
            rows_data.append(stats)
    return rows_data

ladder_I_json = get_ladder_rung('I')
ladder_II_json = get_ladder_rung('II')
ladder_III_json = get_ladder_rung('III')
ladder_IV_json = get_ladder_rung('IV')

all_timelines_json = [
    get_timeline(ladder_I_json),
    get_timeline(ladder_II_json),
    get_timeline(ladder_III_json),
    get_timeline(ladder_IV_json),
]

# Parse all timelines into one dataframe
all_rows = []
for timeline in all_timelines_json:
    all_rows.extend(fill_rank_tl(timeline))

rank_df = pd.DataFrame(all_rows)
