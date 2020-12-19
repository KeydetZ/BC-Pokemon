import argparse
import requests


def error(code, message):
    print("unexpected error {}: {}".format(code, message))
    exit(code)


def get_moves_from_pokemon_by_generation(this_poke, gen):
    if gen:
        for m in this_poke["moves"]:
            # get all generations (version_groups) that his move has been in
            m["version_group_details"] = [x["version_group"]["name"] for x in m["version_group_details"]]
        # filter out moves that are not for the given generation
        this_poke["moves"] = [x for x in this_poke["moves"] if gen in x["version_group_details"]]
    return this_poke["moves"]


# use argparse to simply argument parsing
parser = argparse.ArgumentParser(description="A simple CLI using the RESTful pokemon API (https://pokeapi.co/) to "
                                             "look up Pokemons.",
                                 allow_abbrev=False)  # do not allow abbreviation

# allow one and only one type of lookup: by [id, name, move_type]
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--lookup", help="Lookup by name or id")
group.add_argument("--move-type", type=str, help="Lookup by move type", dest="move_type")

# define optional arguments as filters
parser.add_argument("--generation", type=str, help="Filter result by Pokemon generation")

args = parser.parse_args()

# initialize required properties
pokemon_id = None
pokemon_name = None
move_type = None
generation = None

if args.lookup:
    # TODO: verify length of the id returned by the API
    # assumption: no pokemon has numerical name ;)
    # try to parse the input as integer; if it fails, use as string (pokemon name)
    try:
        pokemon_id = int(args.lookup)
    except ValueError:
        # integer parsing fails. use the input as string
        pokemon_name = args.lookup

    # TODO: debug only
    print(type(args.lookup), args.lookup, type(pokemon_id), pokemon_id, type(pokemon_name), pokemon_name)

elif args.move_type:
    move_type = args.move_type
    print(move_type)
else:
    # unexpected: argparse should make sure at least one argument is passed in
    error(2, "missing argument (--lookup | --move_type)")

# parse additional arguments for filtering
if args.generation:
    generation = args.generation
    # TODO: debug only
    print(generation)

# business logic: lookup pokemon or top 10 commonly used moves
# build a url based on entity that's being looked up
url = "https://pokeapi.co/api/v2/{}/{}"

if pokemon_name:
    entity = "pokemon"
    input_type = "pokemon name"
    input_value = pokemon_name
elif pokemon_id:
    entity = "pokemon"
    input_type = "pokedex"
    input_value = pokemon_id
else:  # move_type
    entity = "type"
    input_type = "move type"
    input_value = move_type

url = url.format(entity, input_value)
res = requests.get(url)

# pass on the API error
if res.status_code != 200:
    # report error on the input
    error(3, "invalid {}: {}".format(input_type, input_value))

if entity == "pokemon":
    this_pokemon = res.json()

    # check if we need additional filtering based on generation
    this_pokemon["moves"] = get_moves_from_pokemon_by_generation(this_pokemon, generation)

    # sort alphabetically
    this_pokemon["moves"] = sorted(this_pokemon["moves"], key=lambda x: x["move"]["name"])

    # transform json into the output format
    result = "name={}, pokedex={}, moves={}".format(this_pokemon["name"], this_pokemon["id"],
                                                    [x["move"]["name"] for x in this_pokemon["moves"]])
    print(result)
else:  # move_type
    this_type = res.json()

    # build a count map of moves, by requesting details of all pokemon with this type
    # NOTE: this could by expensive, because we're making 100+ requests at the same moment
    move_cnt = dict.fromkeys([m["name"] for m in this_type["moves"]], 0)

    # populate the map
    for pokemon in this_type["pokemon"]:
        sub_res = requests.get(pokemon["pokemon"]["url"])
        if sub_res.status_code != 200:
            error(4, "unexpected error when sorting moves by popularity")
        this_pokemon = sub_res.json()
        this_pokemon["moves"] = get_moves_from_pokemon_by_generation(this_pokemon, generation)
        for move in this_pokemon["moves"]:
            move_name = move["move"]["name"]
            if move_name in move_cnt:
                move_cnt[move_name] += 1

    # get top 10 moves
    print([x[0] for x in sorted(move_cnt.items(), key=lambda item: item[1], reverse=True)][:10])
