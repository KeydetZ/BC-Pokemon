from unittest import TestCase
import pokemon
from model.Move import Move


class PokemonUnitTest(TestCase):
    def test_filter_moves_by_generation(self):
        moves = [Move(
            {
                "move": {
                    "name": "transform",
                    "url": "https://pokeapi.co/api/v2/move/144/"
                },
                "version_group_details": [
                    {
                        "level_learned_at": 1,
                        "move_learn_method": {
                            "name": "level-up",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
                        },
                        "version_group": {
                            "name": "red-blue",
                            "url": "https://pokeapi.co/api/v2/version-group/1/"
                        }
                    },
                    {
                        "level_learned_at": 1,
                        "move_learn_method": {
                            "name": "level-up",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
                        },
                        "version_group": {
                            "name": "yellow",
                            "url": "https://pokeapi.co/api/v2/version-group/2/"
                        }
                    }
                ]
            }
        )]
        # return untouched
        self.assertTrue(len(pokemon.filter_moves_by_generation(moves, gen="yellow")) == 1)

        # return no item
        self.assertTrue(len(pokemon.filter_moves_by_generation(moves, gen="crystal")) == 0)

    def test_generate_poke_request(self):
        # simply lookup by name
        test_args = pokemon.parse_arguments("qa", ["--lookup", "pikachu"])
        req = pokemon.generate_poke_request(test_args)

        self.assertEqual(req.input_type, "pokemon name")
        self.assertEqual(req.input_value, "pikachu")
        self.assertEqual(req.entity, "pokemon")
        self.assertIsNone(req.generation)

        # lookup by name with generation
        test_args = pokemon.parse_arguments("qa", ["--lookup", "pikachu", "--generation", "yellow"])
        req = pokemon.generate_poke_request(test_args)

        self.assertIsNotNone(req.generation)

        # invalid: flag conflict
        with self.assertRaises(SystemExit):
            test_args = pokemon.parse_arguments("qa", ["--lookup", "pikachu", "--move-type", "normal"])
            req = pokemon.generate_poke_request(test_args)
