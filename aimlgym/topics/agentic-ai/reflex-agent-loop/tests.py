"""Tests for AG-04 Perceive-Act Loop.

Run:  python -m unittest tests -v
By default the reference solution is tested. To test a learner submission,
set AIMLGYM_TARGET to the module name (e.g. AIMLGYM_TARGET=starter).
"""
import importlib
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
S = importlib.import_module(os.environ.get("AIMLGYM_TARGET", "solution"))


class TestVacuum(unittest.TestCase):
    def test_agent_rules(self):
        self.assertEqual(S.reflex_vacuum_agent(("A", "Dirty")), "Suck")
        self.assertEqual(S.reflex_vacuum_agent(("A", "Clean")), "Right")
        self.assertEqual(S.reflex_vacuum_agent(("B", "Clean")), "Left")

    def test_run(self):
        log, score = S.run(S.reflex_vacuum_agent, S.VacuumWorld({"A": True, "B": True}, "A"), 4)
        self.assertEqual([a for _, a in log], ["Suck", "Right", "Suck", "Left"])
        self.assertEqual(score, 4)

    def test_percepts_logged(self):
        log, _ = S.run(S.reflex_vacuum_agent, S.VacuumWorld({"A": False, "B": True}, "A"), 2)
        self.assertEqual(log, [(("A", "Clean"), "Right"), (("B", "Dirty"), "Suck")])

    def test_world(self):
        w = S.VacuumWorld({"A": True, "B": False}, "B")
        w.execute("Right")
        self.assertEqual(w.percept(), ("B", "Clean"))
        w.execute("Left"); w.execute("Suck")
        self.assertEqual(w.dirt, {"A": False, "B": False})

    def test_unknown_action(self):
        with self.assertRaises(ValueError):
            S.VacuumWorld({"A": False, "B": False}, "A").execute("Fly")

    def test_clean_world_oscillates(self):
        log, score = S.run(S.reflex_vacuum_agent, S.VacuumWorld({"A": False, "B": False}, "A"), 3)
        self.assertEqual([a for _, a in log], ["Right", "Left", "Right"])
        self.assertEqual(score, 3 * (2 - 1))

    def test_input_dict_not_mutated(self):
        d = {"A": True, "B": True}
        S.run(S.reflex_vacuum_agent, S.VacuumWorld(d, "A"), 2)
        self.assertEqual(d, {"A": True, "B": True})


if __name__ == "__main__":
    unittest.main()
