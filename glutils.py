import copy

# Maintain a map of player IDs to names
player_names = {}


def addplayername(id, name):
    if id not in player_names:
        player_names[id] = name


def getplayername(id):
    return player_names.get(id)


# This getentity is a convenience function, independent from everything else.
# Provides the logic for manging a map of objects/dicts/whatever.
# Doesn't have to be a team; I've used this function for parks, etc., too
def getentity(name, team_dict, team_template):
    if name not in team_dict:
        team_dict[name] = copy.deepcopy(team_template)
    return team_dict[name]
