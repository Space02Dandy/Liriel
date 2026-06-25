# Plan de JSON y Datos de Juego

## Objetivo
Definir toda la informacion del juego en archivos JSON locales para que el codigo no tenga reglas quemadas. Este documento describe la estructura, los campos necesarios y el orden de carga.

## Archivos principales

- `data/classes.json`
- `data/subclasses.json`
- `data/species.json`
- `data/backgrounds.json`
- `data/spells.json`
- `data/feats.json`
- `data/weapons.json`
- `data/armor.json`
- `data/equipment.json`

## Principios de diseño

- Cada archivo debe ser legible por humanos y estable para cambios futuros.
- Los objetos se identifican por `slug` unico.
- Las referencias entre archivos usan `slug`, nunca nombres visibles.
- El motor Python valida integridad al arrancar.
- No se repiten datos que puedan derivarse; por ejemplo, los bonos de ataque no viven en JSON, se calculan.

## Orden de carga recomendado

1. `classes.json`
2. `subclasses.json`
3. `species.json`
4. `backgrounds.json`
5. `feats.json`
6. `weapons.json`
7. `armor.json`
8. `equipment.json`
9. `spells.json`

## Esquema general

### 1. `classes.json`

Lista de clases base. Cada entrada debe incluir:

- `slug`
- `name`
- `hit_die`
- `primary_ability`
- `saving_throws`
- `armor_proficiencies`
- `weapon_proficiencies`
- `tool_proficiencies`
- `skill_choices`
- `spellcasting`
- `features_by_level`
- `subclass_level`
- `subclasses`
- `equipment_choices`
- `starting_gold`

Ejemplo minimo:

```json
{
  "slug": "bard",
  "name": "Bardo",
  "hit_die": 8,
  "primary_ability": "CHA",
  "saving_throws": ["DEX", "CHA"],
  "armor_proficiencies": ["light"],
  "weapon_proficiencies": ["simple", "hand_crossbow", "longsword", "rapier", "shortsword"],
  "tool_proficiencies": ["musical_instrument:3"],
  "skill_choices": {
    "count": 3,
    "from": ["Acrobatics", "Arcana", "Deception", "History", "Insight", "Intimidation", "Investigation", "Medicine", "Nature", "Perception", "Performance", "Persuasion", "Religion", "Sleight_of_Hand", "Stealth"]
  },
  "spellcasting": {
    "ability": "CHA",
    "preparation": "known",
    "cantrips_known": {"1": 2, "2": 2},
    "spells_known": {"1": 4, "2": 5},
    "slots": {"1": {"1": 2}, "2": {"1": 3, "2": 1}}
  },
  "features_by_level": {
    "1": ["spellcasting", "bardic_inspiration"],
    "2": ["expertise"],
    "3": ["subclass_choice"]
  },
  "subclass_level": 3,
  "subclasses": ["college_of_glamour", "college_of_lore"],
  "equipment_choices": [
    [{"slug": "rapier", "qty": 1}, {"slug": "diplomat_pack", "qty": 1}],
    [{"slug": "longsword", "qty": 1}, {"slug": "entertainer_pack", "qty": 1}]
  ],
  "starting_gold": 0
}
```

### 2. `subclasses.json`

Cada subclase debe incluir:

- `slug`
- `class_slug`
- `name`
- `description`
- `features_by_level`
- `bonus_spells` si aplica
- `spell_locks` si la subclase modifica la lista de conjuros

Ejemplo:

```json
{
  "slug": "college_of_glamour",
  "class_slug": "bard",
  "name": "Colegio del Glamour",
  "description": "...",
  "features_by_level": {
    "3": ["mantle_of_inspiration", "enthralling_performance"],
    "6": ["mantle_of_majesty"],
    "14": ["unbreakable_majesty"]
  },
  "bonus_spells": []
}
```

### 3. `species.json`

Cada especie debe incluir:

- `slug`
- `name`
- `size`
- `speed`
- `traits`
- `lineages`

Ejemplo:

```json
{
  "slug": "elf",
  "name": "Elfo",
  "size": "Medium",
  "speed": 30,
  "traits": ["darkvision_60", "keen_senses", "fey_ancestry", "trance"],
  "lineages": [
    {
      "slug": "high_elf",
      "name": "Alto Elfo",
      "traits": ["bonus_cantrip"]
    }
  ]
}
```

### 4. `backgrounds.json`

Cada trasfondo debe incluir:

- `slug`
- `name`
- `description`
- `asi_choices` o `asi_profile`
- `origin_feat_slug`
- `skill_proficiencies`
- `tool_proficiencies`
- `equipment`
- `gold`

Ejemplo:

```json
{
  "slug": "criminal",
  "name": "Criminal",
  "description": "...",
  "asi_choices": ["DEX", "CON", "INT"],
  "origin_feat_slug": "alert",
  "skill_proficiencies": ["Stealth", "Deception"],
  "tool_proficiencies": ["thieves_tools"],
  "equipment": [{"slug": "crowbar", "qty": 1}],
  "gold": 50
}
```

### 5. `spells.json`

Cada conjuro debe incluir:

- `slug`
- `name`
- `level`
- `school`
- `ritual`
- `casting_time`
- `range`
- `components`
- `duration`
- `description`
- `higher_level`
- `classes`
- `subclasses`

Ejemplo:

```json
{
  "slug": "magic_missile",
  "name": "Proyectil Magico",
  "level": 1,
  "school": "Evocation",
  "ritual": false,
  "casting_time": "1 action",
  "range": "120 feet",
  "components": {"V": true, "S": true, "M": null},
  "duration": "Instantaneous",
  "description": "...",
  "higher_level": "...",
  "classes": ["wizard", "sorcerer"],
  "subclasses": []
}
```

### 6. `feats.json`

Cada dote debe incluir:

- `slug`
- `name`
- `type` (`origin`, `general`, `epic`)
- `asi`
- `effects`
- `prerequisites`

Ejemplo:

```json
{
  "slug": "alert",
  "name": "Alerta",
  "type": "origin",
  "asi": [{"ability": "DEX", "increase": 1}],
  "effects": {"initiative_bonus": 5, "surprise_immunity": true},
  "prerequisites": []
}
```

### 7. `weapons.json`

Campos sugeridos:

- `slug`
- `name`
- `category`
- `damage_dice`
- `damage_type`
- `properties`
- `weight`
- `cost`

### 8. `armor.json`

Campos sugeridos:

- `slug`
- `name`
- `category`
- `base_ac`
- `dex_bonus_type`
- `strength_requirement`
- `stealth_disadvantage`
- `weight`
- `cost`

### 9. `equipment.json`

Debe reunir:

- paquetes iniciales de clase
- equipo de trasfondo
- equipo general de aventura
- herramientas
- consumibles

## Validacion

El cargador Python debe validar:

- que cada `slug` sea unico
- que `class_slug` de subclases exista en `classes.json`
- que los `feat_slug` de trasfondos existan en `feats.json`
- que las armas y armaduras referenciadas existan
- que los conjuros de clase pertenezcan a la clase correcta

## Recomendacion de implementacion

Crear un `src/data/schema.py` o `src/data/models.py` con dataclasses, luego un `loader.py` por archivo y un `repository.py` unico que centralice todo.
