#!/usr/bin/env python3

import argparse
import requests

from app.model.Pokemon import Pokemon
from app.model.Type import Type
from app.util.PokeRequest import PokeRequest

# Show TOP K moves based on popularity
TOP_K = 10


def error(code, message):
    """Print out an error message and exit with non-zero"""
    print("unexpected error {}: {}".format(code, message))
    exit(code)


def filter_moves_by_generation(this_poke, gen):
    """If generation is specified, filter out moves that don't belong to this generation"""
    if gen:
        # filter out moves that are not for the given generation
        this_poke.moves = [x for x in this_poke.moves if gen in x.generations]


def parse_arguments(mode, test_args):
    """Use argparse to simplify argument parsing.
    If mode == "qa", test_args will be used, instead of args passed by the system
    :return parsed args"""

    parser = argparse.ArgumentParser(description="A simple CLI using the RESTful pokemon API (https://pokeapi.co/) to "
                                                 "look up Pokemons.",
                                     allow_abbrev=False)  # do not allow abbreviation
    # allow one and only one type of lookup: by [id, name, move_type]
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--lookup", help="Lookup by name or id")
    group.add_argument("--move-type", type=str, help="Lookup by move type", dest="move_type")
    # define optional arguments as filters
    parser.add_argument("--generation", type=str, help="Filter result by Pokemon generation")

    if mode == "qa" and test_args is not None:
        return parser.parse_args(args=test_args)

    return parser.parse_args()


def generate_poke_request(args):
    """generate a request object that reflects the requested entity, input type & values, and other optional inputs"""
    entity = None
    input_type = None
    input_value = None
    generation = None

    if args.lookup:
        entity = "pokemon"
        # assumption: no pokemon has numerical name ;)
        # try to parse the input as integer; if it fails, use as string (pokemon name)
        try:
            input_value = int(args.lookup)
            input_type = "pokemon id"
        except ValueError:
            # integer parsing fails. use the input as string
            input_value = args.lookup
            input_type = "pokemon name"
    elif args.move_type:
        entity = "type"
        input_value = args.move_type
        input_type = "move type"
    else:
        # unexpected: argparse should make sure at least one argument is passed in
        error(2, "missing argument (--lookup | --move_type)")

    # parse additional arguments for filtering
    if args.generation:
        generation = args.generation

    return PokeRequest(entity, input_type, input_value, generation=generation)


def process_poke_request(req):
    """Make an API call based on input from PokeRequest"""
    url = req.build_url()
    res = requests.get(url)
    # pass on the API error
    if res.status_code != 200:
        # report error on the input
        error(3, "invalid {}: {}".format(req.input_type, req.input_value))
    return res.json()


def handle_pokemon_response(this_pokemon_json, req):
    """Print the result for a pokemon request"""
    # strip out unnecessary data by putting it into a model
    this_pokemon = Pokemon(this_pokemon_json)
    # check if we need additional filtering based on generation
    filter_moves_by_generation(this_pokemon, req.generation)

    # if there's no move after the filtering, this pokemon never appeared in this generation
    if len(this_pokemon.moves) == 0:
        error(4, "pokemon {} never appeared in generation {}".format(req.input_value, req.generation))

    # sort alphabetically
    this_pokemon.moves = sorted(this_pokemon.moves, key=lambda x: x.name)
    # transform json into the output format
    print(this_pokemon)
    # return pokemon object for test inspection
    return this_pokemon


def handle_type_response(this_type_json, req):
    """Print the result for a move-type request"""
    # print out a warning that this could take a while
    print("Processing request... this could take up to 1 minute")
    # strip out unnecessary data by putting it into a model
    this_type = Type(this_type_json)
    # build a count map of moves, by requesting details of all pokemon with this type
    # NOTE: this could by expensive, because we're making 100+ requests at the same moment
    move_cnt = dict.fromkeys([m for m in this_type.move_names], 0)
    # populate the map by sending a request for every pokemon under this type
    for pokemon in this_type.pokemon_name_url.items():
        sub_res = requests.get(pokemon[1])  # get url
        if sub_res.status_code != 200:
            error(5, "unexpected error when sorting moves by popularity")
        this_pokemon = Pokemon(sub_res.json())
        # apply the generation filter
        filter_moves_by_generation(this_pokemon, req.generation)
        # increment cnt map, if this pokemon uses some of the known moves
        for move in this_pokemon.moves:
            move_name = move.name
            if move_name in move_cnt:
                move_cnt[move_name] += 1

    # get top K moves based on popularity
    print("Top {} moves that are most commonly used:".format(TOP_K))
    res = [x[0] for x in sorted(move_cnt.items(), key=lambda item: item[1], reverse=True)][:TOP_K]
    print(res)
    # return moves list for test inspection
    return res


def run_pokemon(mode="prod", test_args=None):
    """Main entry point. Refactored to take in test arguments for integration test
    :return the result, for test inspection"""
    # parse cmdline arguments. common user errors such as missing input is caught here
    arguments = parse_arguments(mode, test_args)
    # build a request to reflect what the user is requesting for
    poke_request = generate_poke_request(arguments)
    # business logic: lookup pokemon or top 10 commonly used moves
    res_json = process_poke_request(poke_request)
    # route to different business logic based on requests
    if poke_request.entity == "pokemon":
        return handle_pokemon_response(res_json, poke_request)
    elif poke_request.entity == "type":
        return handle_type_response(res_json, poke_request)
    else:
        error(6, "{} lookup is not yet supported")


if __name__ == '__main__':
    run_pokemon()
