import os
import unittest
from unittest import TestCase

from app import pokemon


class PokemonTestIT(TestCase):
    """Integration test is inspired by the following blog post
    http://euccas.github.io/blog/20160807/python-unittest-handle-command-line-arguments.html"""
    def test_lookup_by_name(self):
        args = ["--lookup", "pikachu"]
        res = pokemon.run_pokemon("qa", args)

        # it's pikachu
        self.assertEqual(res.name, "pikachu")
        # with moves
        self.assertTrue(len(res.moves) != 0)
        # sorted
        self.assertTrue(res.moves[0].name.startswith('a'))

    def test_lookup_by_name_with_generation(self):
        args = ["--lookup", "pikachu", "--generation", "yellow"]
        res = pokemon.run_pokemon("qa", args)

        # it's pikachu
        self.assertEqual(res.name, "pikachu")
        # with moves
        self.assertTrue(len(res.moves) != 0)
        # a non-yellow move is no longer there
        self.assertTrue("attract" not in [x.name for x in res.moves])

    def test_lookup_by_id(self):
        args = ["--lookup", "25"]
        res = pokemon.run_pokemon("qa", args)

        # it's pikachu
        self.assertEqual(res.name, "pikachu")
        # with moves
        self.assertTrue(len(res.moves) != 0)
        # sorted
        self.assertTrue(res.moves[0].name.startswith('a'))

    def test_lookup_by_invalid_name(self):
        args = ["--lookup", "pika"]
        # invalid name
        with self.assertRaises(SystemExit):
            res = pokemon.run_pokemon("qa", args)

    def test_lookup_by_invalid_id(self):
        args = ["--lookup", "100000"]
        # invalid id
        with self.assertRaises(SystemExit):
            res = pokemon.run_pokemon("qa", args)

    def test_lookup_by_name_with_invalid_generation(self):
        args = ["--lookup", "lugia", "--generation", "yellow"]
        # pokemon not appearing in the requested generation
        with self.assertRaises(SystemExit):
            res = pokemon.run_pokemon("qa", args)

    def test_move_type(self):
        args = ["--move-type", "normal"]
        res = pokemon.run_pokemon("qa", args)

        # back with TOP_K moves
        self.assertTrue(len(res) == pokemon.TOP_K)

    def test_invalid_move_type(self):
        args = ["--move-type", "norm"]
        with self.assertRaises(SystemExit):
            res = pokemon.run_pokemon("qa", args)

    def test_move_type_with_generation(self):
        args = ["--move-type", "normal", "--generation", "yellow"]
        res = pokemon.run_pokemon("qa", args)

        # back with TOP_K moves
        self.assertTrue(len(res) == pokemon.TOP_K)
        # with a popular move in gen yellow
        self.assertTrue("take-down" in res)
