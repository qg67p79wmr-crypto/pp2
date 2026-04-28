import json

import os

FILE = os.path.join(os.path.dirname(__file__), "leaderboard.json")

def load_leaderboard():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_score(name, score, distance):
    data = {
        "name": name,
        "score": score,
        "distance": distance
    }

    leaderboard = load_leaderboard()
    leaderboard.append(data)

    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)
    leaderboard = leaderboard[:10]

    with open(FILE, "w") as f:
        json.dump(leaderboard, f, indent=2, ensure_ascii=False)