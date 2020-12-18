import argparse

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
    # unexpected
    pass

# parse additional arguments for filtering
if args.generation:
    generation = args.generation
    # TODO: debug only
    print(generation)
