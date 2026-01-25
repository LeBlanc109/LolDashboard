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

    for i , f in enumerate(a, start=1):
            for e in f["events"]:
                    row = {**e, "frame_index": i}
                    rows.append(row)

    events_df = pd.DataFrame(rows)
    return events_df
    