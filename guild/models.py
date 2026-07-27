"""The core Character model.

Three separate TODOs live in this file, for three different days — read
the notes at each one carefully, they're not all unlocked at the same time:

  - Day 1: Character's dunder methods (__repr__, __eq__, __hash__, __lt__,
    __bool__) — same idea as Item in items.py, applied to a class other
    exercises will already be using.
  - Day 4: HealerMixin / TankMixin / LoggableMixin — the mixin & MRO
    workshop.
  - Day 5: GuildMeta — the registry metaclass. Character does NOT use it
    yet (see the class statement below) — wiring it in is literally your
    last Day 5 step, once GuildMeta itself works.

fields.py (StringField/IntField) is already working, so Character's
fields below will validate correctly from Day 1 onward regardless of
which of the above TODOs you've reached.
"""
from __future__ import annotations

from typing import Dict, Type

from .fields import IntField, StringField


class GuildMeta(type):

    registry: Dict[str, Type["Character"]] = {}

    def __new__(mcs, name, bases, namespace, **kwargs):
        new = super().__new__(mcs, name, bases, namespace, **kwargs)

        if bases == ():
            return new

        if not isinstance(getattr(new, "base_hp", None), int):
            raise TypeError(f"{name} must define an int base_hp")

        mcs.registry[name] = new
        return new

class Character(metaclass=GuildMeta):
    """Base class for every playable character."""

    name = StringField(max_length=50)
    hp = IntField(minimum=0)
    level = IntField(minimum=1, maximum=100)

    base_hp: int = 10  # overridden by every concrete subclass

    def __init__(self, name: str, level: int = 1):
        self.name = name
        self.level = level
        self.hp = self.base_hp * level

    def describe_role(self) -> str:
        return "Adventurer"

    # --- Day 1 dunder set -------------------------------------------------

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name='{self.name}', level={self.level}, hp={self.hp})"

    def __str__(self) -> str:
        return f"{self.name} the {self.describe_role()} (Lv.{self.level}, {self.hp} HP)"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Character):
            return NotImplemented

        return (type(other) == type(self)
                and self.name == other.name
                and self.level == other.level)

    def __hash__(self) -> int:
        return hash((type(self), self.name, self.level))

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Character):
            return NotImplemented

        return self.level < other.level

    def __gt__(self, other):
        if not isinstance(other, Character):
            return NotImplemented

        return self.level > other.level

    def __le__(self, other):
        if not isinstance(other, Character):
            return NotImplemented

        return self.level <= other.level

    def __ge__(self, other):
        if not isinstance(other, Character):
            return NotImplemented

        return self.level >= other.level

    def __bool__(self) -> bool:
        return self.hp > 0


class Warrior(Character):
    base_hp = 15

    def describe_role(self) -> str:
        return "Warrior"


class Mage(Character):
    base_hp = 8

    def describe_role(self) -> str:
        return "Mage"


class Rogue(Character):
    base_hp = 10

    def describe_role(self) -> str:
        return "Rogue"


# --- Day 4 mixins: horizontal reuse without deep inheritance ---------------

class HealerMixin:
    heal_power: int = 5

    def describe_role(self) -> str:
        return super().describe_role() + " + Healer"

    def heal(self, target: "Character", amount: int = None) -> int:
        max_hp = target.base_hp * target.level
        healed_hp = target.hp + (amount if amount else self.heal_power)

        return min(healed_hp, max_hp)


class TankMixin:
    taunt_radius: int = 3

    def describe_role(self) -> str:
        return super().describe_role() + " + Tank"

    def taunt(self, enemies) -> list:
        return list(enemies)


class Paladin(HealerMixin, TankMixin, Warrior):
    """The deliberate mixin conflict. Once HealerMixin and TankMixin are
    implemented above, run Paladin.__mro__ and Paladin("x").describe_role()
    and be ready to explain, step by step, why the result is what it is —
    and what would change if TankMixin were listed before HealerMixin in
    the class statement above.
    """

    base_hp = 20


# --- Day 4 (independent mixin, not part of the conflict above) ------------

class LoggableMixin:

    def __init__(self, *args, **kwargs):
        self.__dict__["_log"] = []
        super().__init__(*args, **kwargs)

    def __setattr__(self, name: str, value) -> None:
        if name != "_log":
            self._log.append(f"{name} = {value!r}")
        super().__setattr__(name, value)

    @property
    def log(self) -> list:
        return self._log.copy()


class LoggedMage(LoggableMixin, Mage):
    """Demo combination used by the test suite / workshop walkthrough."""
