import pandas as pd
import requests

def get_ladder_rung(division , auth):
    return requests.get(
        f'https://na1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/SILVER/{division}?page=1&api_key={auth}'
    ).json()

def get_timeline(ladder_json, auth, player_index=15):
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

def second_function(api_key):
    auth = api_key

    ladder_I_json = get_ladder_rung('I', auth)
    ladder_II_json = get_ladder_rung('II', auth)
    ladder_III_json = get_ladder_rung('III', auth)
    ladder_IV_json = get_ladder_rung('IV', auth)

    all_timelines_json = [
        get_timeline(ladder_I_json, auth),
        get_timeline(ladder_II_json, auth),
        get_timeline(ladder_III_json, auth),
        get_timeline(ladder_IV_json, auth),
    ]

    # Parse all timelines into one dataframe
    all_rows = []
    for timeline in all_timelines_json:
        all_rows.extend(fill_rank_tl(timeline))
    
    ranked_df = pd.DataFrame(all_rows)

    lane_template = {
        1: "top", 2: "jungle", 3: "mid", 4: "bot", 5: "supp",
        6: "top", 7: "jungle", 8: "mid", 9: "bot", 10: "supp"
    }
    ranked_df['position'] = ranked_df['participantId'].map(lane_template)
    ranked_df['PBISource'] = 'Silver Average'

    return ranked_df
