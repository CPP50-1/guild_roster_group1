"""Day 2 workshop targets, one per developer:

    Dev A -> OrderedSet      (custom unique-item structure)
    Dev B -> StatCalculator  (memoized callable, state held between calls)
    Dev C -> Roster          (full container protocol + iterator protocol
                              from scratch, i.e. __iter__ returning a real
                              iterator object with __next__, not a generator)

Constructors that just store their arguments are given; the actual
protocol methods are TODOs.
"""
from __future__ import annotations

from typing import Any, Dict, Iterator, List

from .models import Character


# --- Dev A: OrderedSet ------------------------------------------------------

class OrderedSet:
    """A set that remembers insertion order. Backed by a dict (Python 3.7+
    dicts are insertion-ordered) purely for its keys — this is what gives
    O(1) membership instead of the O(n) a list would need. Use only the
    keys of self._data; never store meaningful values in them.
    """

    def __init__(self, items: Iterator[Any] = ()):
        self._data: Dict[Any, None] = {}
        for item in items:
            self.add(item)

    def add(self, item: Any) -> None:
        """TODO (Day 2): add item, no-op if it's already present."""
        raise NotImplementedError("TODO (Day 2): implement OrderedSet.add")

    def discard(self, item: Any) -> None:
        """TODO (Day 2): remove item if present; do nothing if it isn't."""
        raise NotImplementedError("TODO (Day 2): implement OrderedSet.discard")

    def __contains__(self, item: Any) -> bool:
        raise NotImplementedError("TODO (Day 2): implement OrderedSet.__contains__")

    def __iter__(self) -> Iterator[Any]:
        raise NotImplementedError("TODO (Day 2): implement OrderedSet.__iter__")

    def __len__(self) -> int:
        raise NotImplementedError("TODO (Day 2): implement OrderedSet.__len__")

    def __repr__(self) -> str:
        raise NotImplementedError("TODO (Day 2): implement OrderedSet.__repr__")

    def __eq__(self, other: object) -> bool:
        """TODO (Day 2): two OrderedSets are equal if they contain the
        same items in the same order.
        """
        raise NotImplementedError("TODO (Day 2): implement OrderedSet.__eq__")


# --- Dev B: memoized callable ------------------------------------------------

class StatCalculator:
    """A callable object that caches results by argument, for an
    expensive/derived stat computation.
    """

    def __init__(self):
        self._cache: Dict[tuple, int] = {}
        self.calls = 0
        self.cache_hits = 0

    def __call__(self, character: Character, difficulty: int) -> int:
        self.calls += 1
        key = (str(type(character)), character.level, difficulty)
        if key in self._cache:
            self.cache_hits += 1
            return self._cache[key]
        result = (character.level * 7 + difficulty * 13) % 100
        self._cache[key] = result
        return result


# --- Dev C: full container protocol + iterator protocol from scratch -------

class RosterIterator:
    """A standalone iterator object for Roster, built from scratch rather
    than via a generator function — this is what Day 2's "__iter__ and
    __next__ from scratch" specifically asks for.
    """

    def __init__(self, characters: List[Character]):
        self._characters = characters
        self._index = 0

    def __iter__(self) -> "RosterIterator":
        return self

    def __next__(self) -> Character:
        self._index += 1
        if self._index >= len(self._characters):
            raise StopIteration
        character = self._characters[self._index]
        return character


class Roster:
    """A guild's roster of characters, supporting the full container
    protocol: indexing, assignment, deletion, membership, length, and
    iteration.
    """
    def __init__(self, characters: Iterator[Character] = ()):
        self._characters: List[Character] = list(characters)

    def __getitem__(self, index: int) -> Character:
        raise NotImplementedError("TODO (Day 2): implement Roster.__getitem__")

    def __setitem__(self, index: int, value: Character) -> None:
        """TODO (Day 2): reject non-Character values with a TypeError."""
        raise NotImplementedError("TODO (Day 2): implement Roster.__setitem__")

    def __delitem__(self, index: int) -> None:
        raise NotImplementedError("TODO (Day 2): implement Roster.__delitem__")

    def __contains__(self, item: Character) -> bool:
        raise NotImplementedError("TODO (Day 2): implement Roster.__contains__")

    def __len__(self) -> int:
        raise NotImplementedError("TODO (Day 2): implement Roster.__len__")

    def __iter__(self) -> RosterIterator:
        """TODO (Day 2): return a RosterIterator over this roster's
        characters — this is the connection between the container
        protocol and the from-scratch iterator class above.
        """
        raise NotImplementedError("TODO (Day 2): implement Roster.__iter__")

    def __repr__(self) -> str:
        raise NotImplementedError("TODO (Day 2): implement Roster.__repr__")

    def add(self, character: Character) -> None:
        self._characters.append(character)

    def alive_characters(self) -> Iterator[Character]:
        for character in self._characters:
            if character:
                yield character
                
    def sorted_by_level(self) -> List[Character]:
        return sorted(self._characters)
