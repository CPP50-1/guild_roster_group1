"""Day 3, Dev A: a turn-based combat coroutine.

Usage sketch once implemented:

    log = []
    fight = battle(character, log)
    state = next(fight)                # prime the generator
    state = fight.send("attack")       # player acts, generator advances
    state = fight.throw(AmbushError()) # simulate an interrupt mid-battle
    fight.close()                      # abandon the fight cleanly
"""
from __future__ import annotations

from typing import Dict, Generator, List

from .exceptions import GuildError
from .models import Character


class AmbushError(GuildError):
    """Raised into the battle generator to simulate a mid-fight ambush —
    exercises Generator.throw() specifically.
    """


def battle(
        character: Character,
        combat_log: List[str],
        enemy_name: str = "Goblin",
        enemy_hp: int = 30,
        enemy_attack: int = 5,
) -> Generator[Dict, str, None]:
    try:
        combat_log.append(f"{enemy_name} appears!")

        while enemy_hp > 0 and character:
            snapshot = {"character_hp": character.hp, "enemy_hp": enemy_hp}
            action = yield snapshot
            match action:
                case "attack":
                    enemy_hp -= 10
                    combat_log.append(f"{character.name} hits {enemy_name}")
                case "flee":
                    combat_log.append("flees")
                    return
                case "heal":
                    max_health = character.base_hp * character.level
                    character.hp += 15
                    character.hp = min(character.hp, max_health)
                    combat_log.append(f"{character.name} healed")
                case _:
                    combat_log.append(f"{action} is not valid action")
            if enemy_hp > 0:
                character.hp -= enemy_attack
                combat_log.append(f"{enemy_name} hits {character.name}")
            combat_log.append(f"character_hp : {character.hp}")
            combat_log.append(f"enemy_hp : {enemy_hp}")

        yield {"outcome": "victory" if character.hp > 0 else "defeat"}

    except AmbushError:
        combat_log.append(f"Ambush!")
        yield {"ambushed": True}

    finally:
        combat_log.append("Combat generator closed.")
