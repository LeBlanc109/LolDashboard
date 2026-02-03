import pandas as pd
import json

def third_function():
    #a = the list of frames
    #i = frame index
    #f = an individual frame
    #e = an individual event "grouping"

    with open("match_timeline.json", "r") as file:
            data = json.load(file)
    a = data["info"]["frames"]
    rows = []

    for i , f in enumerate(a, start=0):
            for e in f["events"]:
                    row = {**e, "frame_index": i}

                    #seperatin the pos like in lg_stats
                    if "position" in row and isinstance(row["position"], dict):
                        row["x"] = row["position"]["x"]
                        row["y"] = row["position"]["y"]
                    
                    if "assistingParticipantIds" in row and isinstance(row["assistingParticipantIds"], list):
                        row["assistingParticipantIds_str"] = ",".join(str(x) for x in row["assistingParticipantIds"])
                    else:
                        row["assistingParticipantIds_str"] = ""
            
                    # for kp %
                    if e.get("type") == "CHAMPION_KILL":
                        killer_id = e.get("killerId", 0)
                        row["killerTeamId"] = 100 if killer_id <= 5 else 200
                    
                    rows.append(row)

    events_df = pd.DataFrame(rows)
    return events_df
    
#print(third_function().query('type == "CHAMPION_KILL"').dropna(axis="columns"))