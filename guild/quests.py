"""Day 3, Dev B: a quest pipeline built almost entirely from itertools.

The three quest-source generators below are given (they're just static
data). Everything that actually combines/filters/groups them using
itertools is a TODO.
"""
from __future__ import annotations

import itertools
from typing import Dict, Iterable, Iterator, List

from .models import Character

Quest = Dict[str, object]


# --- Static quest sources, given -------------------------------------------

def daily_quests() -> Iterator[Quest]:
    yield {"name": "Clear the Rat Cellar", "reward_gold": 20, "min_level": 1}
    yield {"name": "Escort the Merchant", "reward_gold": 35, "min_level": 2}


def guild_quests() -> Iterator[Quest]:
    yield {"name": "Retrieve the Lost Banner", "reward_gold": 60, "min_level": 3}
    yield {"name": "Defend the Outpost", "reward_gold": 90, "min_level": 5}


def event_quests() -> Iterator[Quest]:
    yield {"name": "Harvest Festival Errand", "reward_gold": 15, "min_level": 1}


def combined_quest_feed() -> Iterator[Quest]:
    return itertools.chain(
        daily_quests(),
        guild_quests(),
        event_quests(),
    )


def endless_bounty_quests() -> Iterator[Quest]:
    for i in itertools.count(start=1):
        yield {
            "name": f"Bounty Contract #{i}",
            "reward_gold": 10 + i * 5,
            "min_level": 1 + i // 3,
        }


def first_n_bounties(n: int) -> List[Quest]:
    return list(itertools.islice(endless_bounty_quests(), n))


def quests_under_budget(quests: Iterable[Quest], budget: int) -> List[Quest]:
    sorted_quests = sorted(quests, key=lambda q: q["reward_gold"])

    return list(itertools.takewhile(lambda q: q["reward_gold"] < budget, sorted_quests))


# --- TODO (Day 3): itertools.groupby -----------------------------------------

def group_roster_by_role(characters: Iterable[Character]) -> Dict[str, List[Character]]:
    """TODO: sort `characters` by describe_role(), then use
    itertools.groupby (also keyed by describe_role()) to build a dict of
    role -> list of characters.

    itertools.groupby only groups *consecutive* runs of the same key —
    without the sort first, characters of the same role that aren't
    adjacent in the input would end up in separate groups.
    """
    raise NotImplementedError("TODO (Day 3): implement group_roster_by_role")


# --- TODO (Day 3): itertools.product -----------------------------------------

def eligible_assignments(
    characters: Iterable[Character], quests: Iterable[Quest]
) -> List[tuple]:
    """TODO: use itertools.product to build every (character, quest) pair,
    then filter down to pairs where character.level >= quest["min_level"].
    """
    raise NotImplementedError("TODO (Day 3): implement eligible_assignments")
