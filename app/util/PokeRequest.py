class PokeRequest:
    # build a url based on entity that's being looked up
    url = "https://pokeapi.co/api/v2/{}/{}"

    def __init__(self, entity, input_type, input_value, generation=None):
        # the entity this request is querying
        self.entity = entity
        # the type of the input value: e.g. pokemon name
        self.input_type = input_type,
        # the input value
        self.input_value = input_value
        # optional filtering on generation
        self.generation = generation

    def build_url(self):
        return PokeRequest.url.format(self.entity, self.input_value)
