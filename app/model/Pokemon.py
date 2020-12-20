from app.model.Move import Move


class Pokemon:
    def __init__(self, pokemon_json, url=None):
        self.name = pokemon_json["name"]
        self.pokedex = pokemon_json["id"]
        self.moves = [Move(x, None) for x in pokemon_json["moves"]]
        self.url = url

    def __repr__(self):
        return """
        name: {}
        pokedex: {}
        moves: {}
        """.format(self.name, self.pokedex, self.moves)
