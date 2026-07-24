"""Day 3, Dev C: two pieces, both TODOs.

1. An infinite dungeon generator built from yield-from delegation to a
   per-floor sub-generator.
2. A contextlib.contextmanager-style transaction. Look at
   exceptions.batch_validation (in exceptions.py) first — it's a complete,
   working example of exactly this pattern (a generator wrapped in
   @contextmanager) — before writing this one from scratch.
"""
from __future__ import annotations

from contextlib import contextmanager
from typing import Dict, Iterator, List


def floor_encounters(floor_number: int, dungeon_log: List[str]) -> Iterator[Dict]:
    dungeon_log.append(f"Entering floor {floor_number}")
    try:
        encounters = [
            {"type": "monster", "floor": floor_number},
            {"type": "loot_chest", "floor": floor_number},
        ]
        if floor_number % 3 == 0:
            encounters.append({"type": "trap", "floor": floor_number})

        for encounter in encounters:
            action = yield encounter
            if action == "retreat":
                dungeon_log.append(f"retreats mid-floor {floor_number}")
                return "retreated"
        dungeon_log.append("Cleared")
        return "cleared"
    finally:
        dungeon_log.append(f"Leaving floor {floor_number}")


def dungeon_floors(dungeon_log: List[str]) -> Iterator[Dict]:
    floor_number = 0
    try:
        while True:
            floor_number += 1
            result = yield from floor_encounters(floor_number, dungeon_log)
            if result == "retreated":
                dungeon_log.append("Party returns to town.")
                return
    finally:
            dungeon_log.append("Dungeon generator closed.")


@contextmanager
def guild_transaction(treasury: Dict[str, int]) -> Iterator[Dict[str, int]]:
    treasury_copy = treasury.copy()
    try:
        yield treasury
    except Exception:
        treasury.clear()
        treasury.update(treasury_copy)
        raise
