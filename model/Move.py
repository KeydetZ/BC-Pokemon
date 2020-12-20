class Move:
    def __init__(self, move_json, url=None):
        self.name = move_json["move"]["name"]
        self.url = url
        # get all generations (version_groups) that this move has been in
        self.generations = [x["version_group"]["name"] for x in move_json["version_group_details"]]

    def __repr__(self):
        return self.name
