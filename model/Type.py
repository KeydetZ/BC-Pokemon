class Type:
    def __init__(self, type_json, url=None):
        self.move_names = [x["name"] for x in type_json["moves"]]
        self.pokemon_name_url = {x["pokemon"]["name"]: x["pokemon"]["url"] for x in type_json["pokemon"]}
        self.url = url
