## Pokemon CLI

Pokemon, also known as "pocket monster" are little creatures with a TV show, a couple cartoon movies, a few videos
games, etc. This is a CLI tool which lookups Pokemon and their moves. The tool is backed by a public RESTful
API (http://pokeapi.co/).

## Setup

* Download this source code into a working directory
* install python3
* [install `pipenv`](https://pipenv.pypa.io/en/latest/install/#installing-pipenv)
* install dependencies: `pipenv sync`
* switch to this environment: `pipenv shell`

## Usage

Examples:

* Lookup Pokemon by name or pokedex. Output name, pokedex and moves, ordered alphabetically
  ```shell
  $ ./pokemon.py --lookup pikachu
  name: pikachu
  pokedex: 25
  moves: [agility, attract, bide, body-slam, brick-break, captivate, charge-beam, confide, counter, covet, curse, defense-curl, detect, dig, discharge, double-edge, double-team, dynamic-punch, echoed-voice, electro-ball, electroweb, endure, facade, feint, flash, fling, focus-punch, frustration, grass-knot, growl, headbutt, helping-hand, hidden-power, iron-tail, knock-off, light-screen, magnet-rise, mega-kick, mega-punch, mimic, mud-slap, natural-gift, nuzzle, pay-day, play-nice, protect, quick-attack, rage, rain-dance, reflect, rest, return, rock-smash, rollout, round, secret-power, seismic-toss, shock-wave, signal-beam, skull-bash, slam, sleep-talk, snore, spark, strength, submission, substitute, surf, swagger, swift, tail-whip, take-down, thunder, thunder-punch, thunder-shock, thunder-wave, thunderbolt, toxic, volt-switch, wild-charge, zap-cannon]
  
  $ ./pokemon.py --lookup 25
  (same as above)
  ```

* Lookup moves by type, order by popularity (most commonly used among Pokemon and their evolutions)
  ```shell
  $ ./pokemon.py --move-type normal
  Processing request... this could take up to 1 minute
  Top 10 moves that are most commonly used:
  ['double-team', 'substitute', 'sleep-talk', 'return', 'frustration', 'hidden-power', 'round', 'confide', 'protect', 'swagger']
  ```

* Apply a filter on generation on any supported lookups
  ```shell
  $ ./pokemon.py --lookup pikachu --generation yellow
  name: pikachu
  pokedex: 25
  moves: [agility, bide, body-slam, double-edge, double-team, flash, growl, light-screen, mega-kick, mega-punch, mimic, pay-day, quick-attack, rage, reflect, rest, seismic-toss, skull-bash, slam, submission, substitute, surf, swift, tail-whip, take-down, thunder, thunder-shock, thunder-wave, thunderbolt, toxic]
  ```

## Assumption

* `pokedex` in the output maps to the Pokemon ID in the API doc. `pokedex` in the API doc refers to an electronic
  encyclopedia device instead.
* The input `generation` maps to `version_group` in the API doc. The API defines `generation` as "a grouping of the
  Pokémon games that separates them based on the Pokémon they include".
* The name of a Pokemon cannot be a number.
* We determine "K most commonly used" moves by scanning through all evolutions of all Pokemon who could have such a
  move, counting and yielding ones with most usages.
    * Many evolution forms of various Pokemons could share the same move.
    * `type` is a common property shared by `pokemon` and `move`
    * Only a subset of Pokemon could possess a type of move, instead of the entire Pokemon group. The subset of Pokemon
      come from the `type` endpoint, where it contains a list of `pokemon` as well as a list of `move` that belong to a
      certain type.

## Test
The project contains an integration and unit test suite, implemented using the standard `unittest` runner.
* `test/unit`
* `test/integration`

## Credit
Some components of this project were made possible by the following blog posts and answers:
1. Make HTTP request in Python: https://requests.readthedocs.io/en/master/
2. Python `argparse` tutorial: https://docs.python.org/3/howto/argparse.html
3. Unit & Integration test: http://euccas.github.io/blog/20160807/python-unittest-handle-command-line-arguments.html
4. Dependency Management: https://pipenv.pypa.io/en/latest/