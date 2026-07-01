# Plan de JSON y Modelos de Datos — Liriel

> **Recordatorio de alcance:** Este documento describe los datos estáticos de reglas del juego.
> Liriel únicamente lee estos datos para construir y calcular hojas de personaje.
> No hay simulación de combate, tirador de dados, ni nada fuera de la hoja.

---

## Objetivo

Definir toda la información de juego en archivos JSON locales para que el código no tenga reglas quemadas.
El motor Python lee estos archivos al arrancar, los valida y los expone a través de un repositorio central.

---

## Archivos de datos de juego

```
data/
├── classes.json        # Clases base (Bardo, Clérigo, Mago…)
├── subclasses.json     # Subclases por clase
├── species.json        # Especies (Elfo, Humano, Tiefling…)
├── backgrounds.json    # Trasfondos (Criminal, Erudito…)
├── feats.json          # Dotes (origen, generales, épicas)
├── spells.json         # Conjuros (todos los niveles)
├── weapons.json        # Armas (simples y marciales)
├── armor.json          # Armaduras y escudos
└── equipment.json      # Equipo general, herramientas y paquetes
```

---

## Principios de diseño

- Cada objeto se identifica con un `slug` único en minúsculas con guiones bajos (ej. `college_of_glamour`).
- Las referencias entre archivos usan siempre `slug`, nunca nombres visibles en pantalla.
- Los valores **derivados** (modificadores, CA, bono de ataque, CD de conjuro) **no se almacenan** en JSON; el motor los calcula.
- Los archivos deben ser legibles por humanos y estables ante cambios futuros.
- Un `loader.py` dedicado valida integridad referencial al arrancar.

---

## Orden de carga obligatorio

El repositorio debe cargar en este orden para resolver referencias:

1. `classes.json`
2. `subclasses.json`  ← referencia `class_slug`
3. `species.json`
4. `backgrounds.json` ← referencia `origin_feat_slug`
5. `feats.json`       ← debe estar antes que backgrounds en validación
6. `weapons.json`
7. `armor.json`
8. `equipment.json`
9. `spells.json`      ← referencia `classes` y `subclasses`

---

## Esquemas detallados

### 1. `classes.json`

Cada entrada describe una clase base completa.

| Campo | Tipo | Descripción |
|---|---|---|
| `slug` | string | Identificador único |
| `name` | string | Nombre en español |
| `hit_die` | int | Caras del dado de golpe (6, 8, 10, 12) |
| `primary_ability` | string | Característica principal (`STR`, `DEX`, etc.) |
| `saving_throws` | list[string] | Las 2 salvaciones de competencia |
| `armor_proficiencies` | list[string] | `light`, `medium`, `heavy`, `shield` |
| `weapon_proficiencies` | list[string] | `simple`, `martial` + armas individuales por slug |
| `tool_proficiencies` | list[string] | Herramientas; el sufijo `:N` indica "elige N" |
| `skill_choices` | object | `{ "count": N, "from": [...] }` |
| `spellcasting` | object \| null | null si la clase no lanza conjuros |
| `features_by_level` | object | `{ "1": ["slug_rasgo", ...], ... }` |
| `subclass_level` | int | Siempre 3 en 5.5e (2024) |
| `subclasses` | list[string] | Lista de slugs de subclases válidas |
| `equipment_choices` | list[list[object]] | Opciones de equipo inicial |
| `starting_gold` | int | Oro alternativo si el jugador elige comprar |
| `asi_levels` | list[int] | Niveles donde se otorga ASI/Dote (varía por clase) |

**Ejemplo mínimo — Bardo:**

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
    "from": ["Acrobatics", "Arcana", "Deception", "History", "Insight",
              "Intimidation", "Investigation", "Medicine", "Nature",
              "Perception", "Performance", "Persuasion", "Religion",
              "Sleight_of_Hand", "Stealth"]
  },
  "spellcasting": {
    "ability": "CHA",
    "preparation": "known",
    "cantrips_known": {"1": 2, "4": 3, "10": 4},
    "spells_known": {"1": 4, "2": 5, "3": 6},
    "slots": {
      "1": {"1": 2},
      "2": {"1": 3, "2": 1},
      "3": {"1": 4, "2": 2, "3": 2}
    }
  },
  "features_by_level": {
    "1": ["spellcasting", "bardic_inspiration"],
    "2": ["expertise", "jack_of_all_trades", "song_of_rest"],
    "3": ["subclass_choice", "expertise"]
  },
  "subclass_level": 3,
  "subclasses": ["college_of_glamour", "college_of_lore", "college_of_valor", "college_of_swords"],
  "equipment_choices": [
    [{"slug": "rapier", "qty": 1}],
    [{"slug": "longsword", "qty": 1}]
  ],
  "starting_gold": 125,
  "asi_levels": [4, 8, 12, 16, 19]
}
```

---

### 2. `subclasses.json`

| Campo | Tipo | Descripción |
|---|---|---|
| `slug` | string | Identificador único |
| `class_slug` | string | Referencia a `classes.json` |
| `name` | string | Nombre visible |
| `description` | string | Descripción breve |
| `features_by_level` | object | Rasgos en qué niveles |
| `bonus_spells` | list[object] | `{ "level": N, "spells": [...slugs] }` si aplica |
| `spell_locks` | list[string] | Conjuros que la subclase bloquea o fija |

```json
{
  "slug": "college_of_glamour",
  "class_slug": "bard",
  "name": "Colegio del Glamour",
  "description": "Bardos que dominan la magia feérica del encantamiento.",
  "features_by_level": {
    "3": ["mantle_of_inspiration", "enthralling_performance"],
    "6": ["mantle_of_majesty"],
    "14": ["unbreakable_majesty"]
  },
  "bonus_spells": [],
  "spell_locks": []
}
```

---

### 3. `species.json`

| Campo | Tipo | Descripción |
|---|---|---|
| `slug` | string | Identificador único |
| `name` | string | Nombre visible |
| `size` | string | `Tiny`, `Small`, `Medium`, `Large` |
| `speed` | int | Velocidad base en pies |
| `traits` | list[string] | Slugs de rasgos innatos |
| `lineages` | list[object] | Sub-razas/linajes opcionales |
| `darkvision` | int \| null | Radio en pies (null si no tiene) |

```json
{
  "slug": "elf",
  "name": "Elfo",
  "size": "Medium",
  "speed": 30,
  "darkvision": 60,
  "traits": ["darkvision", "keen_senses", "fey_ancestry", "trance"],
  "lineages": [
    {
      "slug": "high_elf",
      "name": "Alto Elfo",
      "traits": ["bonus_cantrip", "elf_weapon_training"],
      "extra_speed": 0
    },
    {
      "slug": "wood_elf",
      "name": "Elfo del Bosque",
      "traits": ["mask_of_the_wild", "elf_weapon_training"],
      "extra_speed": 5
    }
  ]
}
```

---

### 4. `backgrounds.json`

| Campo | Tipo | Descripción |
|---|---|---|
| `slug` | string | Identificador único |
| `name` | string | Nombre visible |
| `description` | string | Descripción narrativa |
| `asi_choices` | list[string] | Las 3 características elegibles para el +2/+1 o +1/+1/+1 |
| `origin_feat_slug` | string | Slug de la dote de origen otorgada |
| `skill_proficiencies` | list[string] | Exactamente 2 habilidades fijas |
| `tool_proficiencies` | list[string] | 1 herramienta fija |
| `equipment` | list[object] | Equipo inicial `{ "slug": ..., "qty": N }` |
| `gold` | int | Siempre 50 po en 5.5e 2024 |

```json
{
  "slug": "criminal",
  "name": "Criminal",
  "description": "Eras un ladrón o contrabandista que vivía al margen de la ley.",
  "asi_choices": ["DEX", "CON", "INT"],
  "origin_feat_slug": "alert",
  "skill_proficiencies": ["Stealth", "Deception"],
  "tool_proficiencies": ["thieves_tools"],
  "equipment": [
    {"slug": "crowbar", "qty": 1},
    {"slug": "common_clothes", "qty": 1}
  ],
  "gold": 50
}
```

---

### 5. `feats.json`

| Campo | Tipo | Descripción |
|---|---|---|
| `slug` | string | Identificador único |
| `name` | string | Nombre visible |
| `type` | string | `origin`, `general`, `epic` |
| `asi` | list[object] | `{ "ability": "DEX", "increase": 1 }` por cada bono de atributo |
| `effects` | object | Efectos mecánicos en clave-valor (ver nota abajo) |
| `prerequisites` | list[string] | Condiciones de requisito en texto o slug |
| `description` | string | Descripción completa |

**Nota sobre `effects`:** El motor interpreta las claves de `effects` para calcular la hoja. Las claves estándar son:
`initiative_bonus`, `surprise_immunity`, `extra_attack`, `bonus_cantrips`, `skill_proficiency`, `tool_proficiency`, `armor_proficiency`, `weapon_proficiency`, `damage_bonus`, `hp_per_level`, `spell_slug`.

```json
{
  "slug": "alert",
  "name": "Alerta",
  "type": "origin",
  "description": "Siempre en guardia, ganas ventaja en iniciativa.",
  "asi": [{"ability": "DEX", "increase": 1}],
  "effects": {
    "initiative_bonus": 5,
    "surprise_immunity": true
  },
  "prerequisites": []
}
```

```json
{
  "slug": "ability_score_improvement",
  "name": "Mejora de Puntuación de Característica",
  "type": "general",
  "description": "Sube una característica en +2 o dos en +1.",
  "asi": [],
  "effects": {
    "asi_flexible": true,
    "asi_points": 2
  },
  "prerequisites": []
}
```

---

### 6. `spells.json`

| Campo | Tipo | Descripción |
|---|---|---|
| `slug` | string | Identificador único |
| `name` | string | Nombre en español |
| `level` | int | 0 (truco) a 9 |
| `school` | string | `Abjuration`, `Conjuration`, `Divination`, etc. |
| `ritual` | bool | Si puede lanzarse como ritual |
| `casting_time` | string | `1 action`, `1 bonus action`, `1 minute`, etc. |
| `range` | string | `Self`, `Touch`, `30 feet`, etc. |
| `components` | object | `{ "V": bool, "S": bool, "M": string \| null }` |
| `duration` | string | `Instantaneous`, `1 minute`, `Concentration, up to 1 hour`, etc. |
| `concentration` | bool | Separado del campo duration para filtrado rápido |
| `description` | string | Texto completo del conjuro |
| `higher_level` | string \| null | Efecto al lanzar con ranura superior |
| `classes` | list[string] | Clases que tienen el conjuro en su lista |
| `subclasses` | list[string] | Subclases que añaden el conjuro extra |
| `tags` | list[string] | Etiquetas opcionales (`damage`, `healing`, `control`, etc.) |

```json
{
  "slug": "magic_missile",
  "name": "Proyectil Mágico",
  "level": 1,
  "school": "Evocation",
  "ritual": false,
  "casting_time": "1 action",
  "range": "120 feet",
  "components": {"V": true, "S": true, "M": null},
  "duration": "Instantaneous",
  "concentration": false,
  "description": "Creas tres proyectiles brillantes...",
  "higher_level": "Por cada espacio de nivel superior al 1.°, un proyectil adicional.",
  "classes": ["wizard", "sorcerer"],
  "subclasses": [],
  "tags": ["damage", "force"]
}
```

---

### 7. `weapons.json`

| Campo | Tipo | Descripción |
|---|---|---|
| `slug` | string | Identificador único |
| `name` | string | Nombre en español |
| `category` | string | `simple_melee`, `simple_ranged`, `martial_melee`, `martial_ranged` |
| `damage_dice` | string | `1d6`, `1d8`, `2d6`, etc. |
| `damage_type` | string | `piercing`, `slashing`, `bludgeoning` |
| `properties` | list[string] | `finesse`, `versatile`, `thrown`, `two_handed`, `light`, `reach`, `ammunition`, `loading` |
| `range` | object \| null | `{ "normal": N, "long": N }` para armas a distancia |
| `weight` | float | Peso en libras |
| `cost` | string | `15 gp`, `2 sp`, etc. |
| `versatile_damage` | string \| null | Daño a dos manos si `versatile` |

---

### 8. `armor.json`

| Campo | Tipo | Descripción |
|---|---|---|
| `slug` | string | Identificador único |
| `name` | string | Nombre en español |
| `category` | string | `light`, `medium`, `heavy`, `shield` |
| `base_ac` | int | CA base sin modificadores |
| `dex_bonus_type` | string | `full` (ligera), `max2` (media), `none` (pesada), `none` (escudo) |
| `strength_requirement` | int \| null | Req. mínimo de FUE (o null) |
| `stealth_disadvantage` | bool | Si impone desventaja en Sigilo |
| `weight` | float | Peso en libras |
| `cost` | string | Precio |

---

### 9. `equipment.json`

Reúne tres categorías en el mismo archivo usando el campo `category`:

| Categoría | Descripción |
|---|---|
| `pack` | Paquetes de equipo inicial (Mochila de Explorador, Paquete de Erudito…) |
| `tool` | Herramientas (ladrones, hierbas, instrumentos musicales…) |
| `gear` | Equipo aventurero general (antorcha, cuerda, ración…) |
| `consumable` | Pociones y objetos consumibles básicos |

```json
{
  "slug": "explorer_pack",
  "name": "Mochila de Explorador",
  "category": "pack",
  "contents": [
    {"slug": "backpack", "qty": 1},
    {"slug": "bedroll", "qty": 1},
    {"slug": "ration", "qty": 10},
    {"slug": "torch", "qty": 10},
    {"slug": "rope_hempen_50ft", "qty": 1},
    {"slug": "waterskin", "qty": 1}
  ],
  "weight": 59,
  "cost": "10 gp"
}
```

---

## Validación al arrancar

El `loader.py` debe validar en este orden:

1. **Slugs únicos** dentro de cada archivo y globalmente en `spells.json`.
2. **Referencias de subclases:** cada `class_slug` debe existir en `classes.json`.
3. **Referencias de trasfondos:** cada `origin_feat_slug` debe existir en `feats.json`.
4. **Referencias de conjuros:** cada clase/subclase en `spells.json[classes]` debe existir en los JSON correspondientes.
5. **Referencias de equipo:** cada slug de `equipment_choices` en clases debe existir en `weapons.json`, `armor.json` o `equipment.json`.
6. **ASI en dotes:** el campo `asi` debe tener abilities válidas (STR, DEX, CON, INT, WIS, CHA).
7. **Niveles de subclase:** debe ser 3 para todas las clases en 5.5e 2024.

Si cualquier validación falla, el programa debe lanzar un `DataIntegrityError` con el slug y la referencia rota, y **no arrancar**.

---

## Capa de modelos Python (`src/data/models.py`)

Usar `dataclasses` para tipar todos los objetos de juego:

```python
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
    skill_choices: dict          # {"count": int, "from": list[str]}
    spellcasting: dict | None
    features_by_level: dict      # {"1": [str, ...], ...}
    subclass_level: int
    subclasses: list[str]
    equipment_choices: list
    starting_gold: int
    asi_levels: list[int]
```

Modelos similares para: `SubclassData`, `SpeciesData`, `BackgroundData`, `FeatData`, `SpellData`, `WeaponData`, `ArmorData`, `EquipmentData`.

---

## Repositorio central (`src/data/repository.py`)

Clase `GameDataRepository` con interfaz de consulta:

```python
class GameDataRepository:
    def get_class(self, slug: str) -> ClassData: ...
    def get_subclasses_for_class(self, class_slug: str) -> list[SubclassData]: ...
    def get_species(self, slug: str) -> SpeciesData: ...
    def get_background(self, slug: str) -> BackgroundData: ...
    def get_feat(self, slug: str) -> FeatData: ...
    def get_spells_for_class(self, class_slug: str, max_level: int) -> list[SpellData]: ...
    def get_weapon(self, slug: str) -> WeaponData: ...
    def get_armor(self, slug: str) -> ArmorData: ...
    def list_classes(self) -> list[ClassData]: ...
    def list_backgrounds(self) -> list[BackgroundData]: ...
    def list_species(self) -> list[SpeciesData]: ...
```

El repositorio es **singleton** inicializado una vez al arrancar. La UI y el motor nunca leen JSON directamente; siempre van a través del repositorio.
