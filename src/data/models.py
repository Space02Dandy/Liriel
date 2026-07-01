from dataclasses import dataclass, field
from typing import Any

@dataclass
class ClassData:
    slug: str
    name: str
    hit_die: int
    primary_ability: str
    saving_throws: list[str]
    armor_proficiencies: list[str]
    weapon_proficiencies: list[str]
    tool_proficiencies: list[str]
    skill_choices: dict
    spellcasting: dict | None
    features_by_level: dict
    subclass_level: int
    subclasses: list[str]
    equipment_choices: list[list[dict]]
    starting_gold: int
    asi_levels: list[int]
    multiclass_requirements: list[dict]

@dataclass
class SubclassData:
    slug: str
    class_slug: str
    name: str
    description: str
    features_by_level: dict
    bonus_spells: list[dict]
    spell_locks: list[str]

@dataclass
class SpeciesData:
    slug: str
    name: str
    size: str
    speed: int
    traits: list[str]
    lineages: list[dict]
    darkvision: int | None
    languages: list[str] = field(default_factory=list)  # Idiomas adicionales que otorga la especie

@dataclass
class BackgroundData:
    slug: str
    name: str
    description: str
    # Las 3 características elegibles para ASI (+2/+1 o +1/+1/+1). Fuente: PHB 2024 p. 3683.
    asi_choices: list[str]
    origin_feat_slug: str
    skill_proficiencies: list[str]
    tool_proficiencies: list[str]
    # Opción A de equipo (lista de objetos). Opción B = siempre 50 po (campo gold).
    equipment: list[dict]
    gold: int
    # Idiomas que otorga el trasfondo (generalmente 2, elegidos de la tabla Estándar).
    languages: list[str] = field(default_factory=list)

@dataclass
class FeatData:
    slug: str
    name: str
    type: str
    asi: list[dict]
    effects: dict
    prerequisites: list[str]
    description: str

@dataclass
class SpellData:
    slug: str
    name: str
    level: int
    school: str
    ritual: bool
    casting_time: str
    range: str
    components: dict
    duration: str
    concentration: bool
    description: str
    higher_level: str | None
    classes: list[str]
    subclasses: list[str]
    tags: list[str]

@dataclass
class WeaponData:
    slug: str
    name: str
    category: str
    damage_dice: str
    damage_type: str
    properties: list[str]
    range: dict | None
    weight: float
    cost: str
    versatile_damage: str | None

@dataclass
class ArmorData:
    slug: str
    name: str
    category: str
    base_ac: int
    dex_bonus_type: str
    strength_requirement: int | None
    stealth_disadvantage: bool
    weight: float
    cost: str

@dataclass
class EquipmentData:
    slug: str
    name: str
    category: str
    weight: float
    cost: str
    contents: list[dict] | None = None