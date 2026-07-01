# Plan de Implementación de Liriel

> **Recordatorio de alcance:** Liriel es ÚNICA Y EXCLUSIVAMENTE un Constructor y Gestor de
> Hojas de Personaje para D&D 5.5e. NO es un VTT, NO tiene combate en tiempo real,
> NO tiene tirador de dados interactivo. Cada fase construye solo funcionalidad de hoja.

---

## Objetivo

Aplicación de escritorio gratuita y open-source para gestionar hojas de personaje completas
de D&D 5.5e (Revisión 2024) usando **Python + PySide6** y assets de pixel art propios.

---

## Decisión técnica principal

| Capa | Tecnología | Razón |
|---|---|---|
| GUI | PySide6 | Licencia LGPL, maduro, buen soporte de pixel art con `QPainter` |
| Lógica de reglas | Python puro | Testeable sin Qt, sin acoplamiento |
| Datos de juego | JSON locales en `data/` | Legibles, sin base de datos |
| Persistencia | `.liriel` (JSON renombrado) en `characters/` | Un archivo por personaje |
| Tests | pytest + pytest-qt | Cubre tanto el motor como la UI |
| Distribución | PyInstaller | Ejecutable sin instalar Python |

---

## Arquitectura — Reglas de separación

```
┌──────────────┐       ┌──────────────────┐       ┌───────────────┐
│  src/ui/     │──────▶│  src/engine/     │──────▶│  src/data/    │
│  (PySide6)   │ señal │  (Python puro)   │ repo  │  (JSON+models)│
└──────────────┘       └──────────────────┘       └───────────────┘
```

- **La UI nunca calcula reglas de D&D.** Solo llama al motor y refresca widgets.
- **El motor nunca importa PySide6.** Solo recibe datos y devuelve resultados.
- **Todos los datos del juego vienen de JSON.** No hay reglas quemadas en código.
- **Cada cambio de personaje pasa por el motor** → luego refresca la UI.
- **Todo cálculo derivado es testeable** sin abrir ventana.

---

## Estructura del proyecto

```
Liriel/
├── main.py                    # Punto de entrada
├── requirements.txt
├── data/                      # JSON de reglas del juego (estáticos)
│   ├── classes/               # Un .json por clase base (12 archivos)
│   │   ├── barbarian.json
│   │   ├── bard.json
│   │   └── …  (wizard.json, etc.)
│   ├── subclasses/            # Subcarpeta por clase, un .json por subclase
│   │   ├── barbarian/
│   │   │   ├── senda_del_berserker.json
│   │   │   └── …  (4 archivos)
│   │   ├── bard/  (…4 archivos)
│   │   └── …  (12 carpetas, 48 archivos en total)
│   ├── species.json
│   ├── backgrounds.json
│   ├── feats.json
│   ├── spells.json
│   ├── weapons.json
│   ├── armor.json
│   └── equipment.json
├── assets/                    # Sprites, iconos, fuentes pixel art
│   ├── icons/
│   ├── sprites/
│   └── fonts/
├── characters/                # Archivos .liriel guardados por el usuario
├── src/
│   ├── data/                  # Modelos, loaders y repositorio
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── loader.py
│   │   └── repository.py
│   ├── engine/                # Motor de reglas puro
│   │   ├── __init__.py
│   │   ├── enums.py
│   │   ├── character.py       # CharacterState
│   │   ├── factory.py         # CharacterFactory (creación)
│   │   ├── progression.py     # LevelUpEngine
│   │   ├── combat.py          # CA, iniciativa (solo cálculos pasivos)
│   │   ├── spellcasting.py    # Slots, conjuros conocidos/preparados
│   │   ├── validation.py      # Validación de elecciones
│   │   └── retroactivity.py   # Recálculo retroactivo CON
│   ├── ui/                    # Capa visual PySide6
│   │   ├── __init__.py
│   │   ├── app.py             # QApplication y QMainWindow
│   │   ├── theme.py           # Paleta dark fantasy, QSS, fuentes
│   │   ├── pixel_art.py       # Utilidades QPainter pixel-perfect
│   │   ├── navigation.py      # Gestión de pantallas/escenas
│   │   ├── scenes/
│   │   │   ├── main_menu.py
│   │   │   ├── creation_wizard.py
│   │   │   ├── character_sheet.py
│   │   │   ├── level_up_scene.py
│   │   │   └── inventory_scene.py
│   │   └── widgets/
│   │       ├── pixel_label.py
│   │       ├── pixel_button.py
│   │       ├── pixel_panel.py
│   │       ├── stat_widget.py
│   │       ├── skill_widget.py
│   │       └── spell_widget.py
│   └── utils/
│       ├── __init__.py
│       └── file_io.py         # Guardar/cargar .liriel
├── tests/
│   ├── test_smoke.py
│   ├── test_loader.py
│   ├── test_factory.py
│   ├── test_progression.py
│   ├── test_retroactivity.py
│   └── test_spellcasting.py
└── scripts/
    └── test_creation.py       # Script de consola para generar personajes de prueba
```

---

## Orden real de implementación (referencia global)

1. `enums.py`
2. `models.py`
3. `loader.py`
4. `repository.py`
5. JSON mínimos funcionales (todas las clases del SRD)
6. `character.py` (CharacterState)
7. `combat.py` (CA e iniciativa pasivos)
8. `spellcasting.py`
9. `validation.py`
10. `factory.py` (CharacterFactory nivel 1)
11. `progression.py` (LevelUpEngine)
12. `retroactivity.py`
13. `file_io.py`
14. `theme.py` + `pixel_art.py`
15. `app.py` + `navigation.py`
16. `main_menu.py`
17. Widgets base (`pixel_button`, `stat_widget`, etc.)
18. `creation_wizard.py`
19. `character_sheet.py`
20. `level_up_scene.py`
21. `inventory_scene.py`
22. Assets finales (Aseprite)
23. Tests de integración completos
24. Empaquetado con PyInstaller

---

## Fase 0 — Preparación del proyecto

**Objetivo:** Repositorio listo para trabajar sin bloqueos.

### Estado actual ✅
- `main.py` abre una ventana PySide6 vacía.
- `requirements.txt` con PySide6, pytest, pytest-qt, pyinstaller.
- Estructura `src/data`, `src/engine`, `src/ui`, `src/utils` creada.
- `.gitignore` presente.

### Tareas pendientes

- [ ] Verificar que `main.py` abre sin errores (`python main.py`).
- [ ] Verificar que `pytest` pasa con un `test_smoke.py` básico.
- [ ] Confirmar que el `.gitignore` excluye `characters/`, `build/`, `dist/`, `.venv/`.

### Resultado esperado
El proyecto abre y el entorno ejecuta tests sin fallar.

---

## Fase 1 — Base de datos JSON y cargador

**Objetivo:** Leer todas las reglas del juego desde archivos estáticos y validarlas.

### Tareas — Motor

- [ ] Crear `src/engine/enums.py`:
  - `Ability` (STR, DEX, CON, INT, WIS, CHA)
  - `Skill` (todas las 18 habilidades de 5.5e)
  - `ArmorCategory` (light, medium, heavy, shield)
  - `WeaponCategory` (simple_melee, simple_ranged, martial_melee, martial_ranged)
  - `SpellSchool` (Abjuration, Conjuration, Divination, Enchantment, Evocation, Illusion, Necromancy, Transmutation)
  - `FeatType` (origin, general, epic)
  - `CreatureSize` (Tiny, Small, Medium, Large, Huge, Gargantuan)
  - `DamageType` (acid, bludgeoning, cold, fire, force, lightning, necrotic, piercing, poison, psychic, radiant, slashing, thunder)
  - `SpellPreparation` (known, prepared)

### Tareas — Modelos y cargador

- [ ] Crear `src/data/models.py` con dataclasses:
  - `ClassData`, `SubclassData`, `SpeciesData`, `BackgroundData`
  - `FeatData`, `SpellData`, `WeaponData`, `ArmorData`, `EquipmentData`
- [ ] Crear `src/data/loader.py` con una función por archivo:
  - `load_classes() -> dict[str, ClassData]`
  - `load_subclasses() -> dict[str, SubclassData]`
  - `load_species() -> dict[str, SpeciesData]`
  - `load_backgrounds() -> dict[str, BackgroundData]`
  - `load_feats() -> dict[str, FeatData]`
  - `load_spells() -> dict[str, SpellData]`
  - `load_weapons() -> dict[str, WeaponData]`
  - `load_armor() -> dict[str, ArmorData]`
  - `load_equipment() -> dict[str, EquipmentData]`
  - Función `validate_all(repo)` que lanza `DataIntegrityError` si hay referencias rotas.
- [ ] Crear `src/data/repository.py` con `GameDataRepository` (singleton, interfaz documentada en `plan_desarrollo_dnd_json.md`).

### Tareas — Archivos JSON

- [ ] `data/classes.json` — Incluir al menos: Bárbaro, Bardo, Clérigo, Druida, Guerrero, Monje, Paladín, Explorador, Pícaro, Hechicero, Brujo, Mago.
  - **⚠️ Multiclaseo:** Cada clase debe incluir el campo `multiclass_requirements` (ver Fase 1 nota abajo).
- [ ] `data/subclasses.json` — 2-3 subclases por clase (las del SRD 2024).
- [ ] `data/species.json` — Humano, Elfo, Enano, Halfling, Gnomo, Semiorco, Tiefling, Draconiano.
- [ ] `data/backgrounds.json` — Al menos 10 trasfondos del manual básico 2024.
- [ ] `data/feats.json` — Todas las dotes de origen + dotes generales del SRD.
- [ ] `data/weapons.json` — Todas las armas simples y marciales del SRD.
- [ ] `data/armor.json` — Todas las armaduras y escudo del SRD.
- [ ] `data/equipment.json` — Paquetes de clase, herramientas, equipo básico.
- [ ] `data/spells.json` — Conjuros del SRD niveles 0-9 (mínimo 50 conjuros representativos por escuela).

> **Nota multiclaseo — `multiclass_requirements` en `classes.json`:**
> Cada entrada de clase debe añadir el campo:
> ```json
> "multiclass_requirements": [
>   {"ability": "STR", "min_score": 13}
> ]
> ```
> Puede ser una lista vacía `[]` si la clase no tiene requisito (ej. Mago sí requiere INT 13).
> Algunos ejemplos:
> | Clase | Requisito |
> |---|---|
> | Bárbaro | STR 13 |
> | Bardo | CHA 13 |
> | Clérigo | WIS 13 |
> | Druida | WIS 13 |
> | Guerrero | STR 13 **o** DEX 13 |
> | Monje | DEX 13 **y** WIS 13 |
> | Paladín | STR 13 **y** CHA 13 |
> | Explorador | DEX 13 **y** WIS 13 |
> | Pícaro | DEX 13 |
> | Hechicero | CHA 13 |
> | Brujo | CHA 13 |
> | Mago | INT 13 |
>
> Para requisitos con **o** lógico (ej. Guerrero), usar `"operator": "OR"` en la lista.
> El `ClassData` en `models.py` debe incluir `multiclass_requirements: list[dict]`.

### Tareas — Tests

- [ ] `tests/test_loader.py`:
  - Verificar que todos los JSON cargan sin excepción.
  - Verificar que el recuento de objetos es correcto (≥ N por tipo).
  - Verificar slugs únicos.
  - Verificar que todas las clases tienen el campo `multiclass_requirements`.
- [ ] `tests/test_loader.py` — tests de referencias cruzadas:
  - `class_slug` de subclases existe en clases.
  - `origin_feat_slug` de trasfondos existe en dotes.
  - Clases en `spells.json` existen en `classes.json`.

### Resultado esperado
El proyecto arranca, carga datos y detecta cualquier error de contenido antes de mostrar UI.

---

## Fase 2 — Modelo de personaje

**Objetivo:** Objeto central `CharacterState` que representa una hoja de personaje completa con soporte nativo de multiclaseo.

### Tareas

- [ ] Definir la estructura auxiliar `ClassEntry` en `src/engine/character.py`:

```python
@dataclass
class ClassEntry:
    """
    Representa un nivel en una clase específica.
    El personaje puede tener varios ClassEntry (uno por clase multiclaseada).
    """
    class_slug: str          # Referencia al slug en classes.json
    level: int               # Niveles alcanzados en ESTA clase (1-20)
    subclass_slug: str | None  # None hasta que el jugador elige en nivel 3 de clase
    hit_dice_rolled: list[int]  # Resultado de cada tirada de dado de golpe en esta clase
                                 # len(hit_dice_rolled) == level
```

- [ ] Crear `CharacterState` usando `class_levels` en lugar de `class_slug`/`subclass_slug`/`level`:

```python
@dataclass
class CharacterState:
    # Identidad
    name: str
    class_levels: list[ClassEntry]   # ← MULTICLASEO: una entrada por clase tomada
    species_slug: str
    lineage_slug: str | None
    background_slug: str

    # Puntuaciones de característica (base + todos los ASI acumulados)
    ability_scores: dict[str, int]   # {"STR": 16, "DEX": 14, ...}

    # Salud
    hp_max: int
    hp_current: int
    hp_temp: int

    # Equipo activo
    armor_slug: str | None
    shield_equipped: bool
    weapons: list[str]               # slugs de armas equipadas
    inventory: list[dict]            # [{"slug": str, "qty": int}, ...]

    # Conjuros
    # Organizado por clase: cada clave es un class_slug lanzador.
    # Permite que Mago y Bardo tengan listas separadas en un multiclase.
    spells_known: dict[str, list[str]]   # {"bard": [slugs...], "wizard": [slugs...]}
    spells_prepared: dict[str, list[str]] # ídem para clases que preparan
    # Slots compartidos entre todas las clases (regla de multiclaseo)
    # Los Warlock slots van aparte: warlock_slots_max + warlock_slots_used
    spell_slots_used: dict[str, int]     # {"1": N, "2": N, ...} slots combinados gastados
    warlock_slots_max: int               # 0 si no hay Brujo
    warlock_slots_used: int              # 0 si no hay Brujo
    warlock_slot_level: int              # Nivel de los slots de Magia de Pacto (1-5)

    # Opciones acumuladas (de todas las clases + trasfondo + especie)
    skill_proficiencies: list[str]
    tool_proficiencies: list[str]
    saving_throw_proficiencies: list[str]
    feats: list[str]                     # slugs de dotes tomadas

    # Metadatos
    xp: int
    created_at: str                      # ISO 8601
    updated_at: str
```

- [ ] Implementar **propiedades calculadas** (no almacenadas, derivadas de `class_levels`):
  - `total_level() -> int` → `sum(e.level for e in class_levels)` ← **clave para multiclaseo**
  - `level_in_class(class_slug: str) -> int` → 0 si el personaje no tiene esa clase
  - `primary_class() -> ClassEntry` → la clase con más niveles (o la primera si empate)
  - `ability_modifier(ability: str) -> int` → `floor((score - 10) / 2)`
  - `proficiency_bonus() -> int` → escala con `total_level()`, NO con nivel de clase
  - `initiative() -> int` → modificador DEX
  - `ac() -> int` → según armadura equipada + DEX + escudo
  - `saving_throw(ability: str) -> int` → mod + PB si competente en alguna de las clases
  - `skill_bonus(skill: str) -> int` → mod + PB si competente
  - `weapon_attack_bonus(weapon_slug: str) -> int`
  - `weapon_damage_bonus(weapon_slug: str) -> int`

- [ ] Implementar `to_dict() -> dict` y `from_dict(d: dict) -> CharacterState`.
  - `class_levels` debe serializarse como lista de dicts `{"class_slug": ..., "level": ..., "subclass_slug": ..., "hit_dice_rolled": [...]}`.
- [ ] Crear `src/utils/file_io.py`:
  - `save_character(character: CharacterState, path: Path) -> None`
  - `load_character(path: Path) -> CharacterState`
  - Formato: JSON con extensión `.liriel`
- [ ] Tests de serialización:
  - Personaje monoclase: guardado y recargado idéntico.
  - Personaje multiclase (Bardo 3 / Guerrero 2): `class_levels` se serializa y deserializa correctamente.
- [ ] Tests de propiedades calculadas:
  - Bardo 4 / Guerrero 1 → `total_level() == 5`, `proficiency_bonus() == 3`.
  - Mago 3 / Clérigo 1 → `level_in_class('wizard') == 3`, `level_in_class('paladin') == 0`.

### Resultado esperado
Un personaje puede existir en memoria, serializar a disco y recuperarse intacto, tanto monoclase como multiclase.

---

## Fase 3 — Motor de creación (Nivel 1)

**Objetivo:** Construir un personaje nivel 1 completamente funcional solo con motor Python.

### Tareas

- [ ] Crear `src/engine/validation.py`:
  - `validate_skill_choices(class_slug, chosen_skills, repo) -> bool`
  - `validate_asi_choices(background_slug, chosen_abilities, repo) -> bool`
  - `validate_equipment_choice(class_slug, choice_index, repo) -> bool`
  - `validate_feat_prerequisites(feat_slug, character, repo) -> bool`
  - `validate_multiclass_requirements(target_class_slug, character, repo) -> bool`
    → Verifica que el personaje cumple los requisitos de atributo de la nueva clase.
    → Verifica que el personaje no supera el nivel 20 total al añadir esta clase.
    → Devuelve `False` con mensaje de error si el requisito no se cumple.

- [ ] Crear `src/engine/combat.py` (solo cálculos pasivos para la hoja):
  - `calculate_ac(character: CharacterState, repo: GameDataRepository) -> int`
  - `calculate_initiative(character: CharacterState) -> int`
  - `calculate_weapon_attack(character, weapon_slug, repo) -> tuple[int, str]`
    → devuelve (bono_total, cadena_daño) ej: `(+5, "1d8+3")`

- [ ] Crear `src/engine/spellcasting.py` con soporte de multiclaseo:
  - `get_single_class_caster_level(class_slug: str, class_level: int, repo) -> float`
    → Devuelve el nivel efectivo de lanzador para una clase:
    → Lanzadores completos (Bardo, Clérigo, Druida, Mago, Hechicero): `class_level × 1.0`
    → Medio lanzadores (Explorador, Paladín): `class_level × 0.5`
    → Lanzadores de un tercio (Guerrero con Caballero Arcano, Pícaro con Embaucador Arcano): `class_level × 0.333` (solo si subclase seleccionada)
    → Brujo: no cuenta para la suma combinada (tiene su propio pool)
    → No lanzadores: `0`
  - `calculate_combined_spell_slots(character: CharacterState, repo) -> dict[str, int]`
    → Suma los niveles efectivos de todas las clases lanzadoras usando `get_single_class_caster_level()`.
    → El total (redondeado hacia abajo) se usa como índice en la tabla de progresión de lanzador completo.
    → Devuelve el diccionario de slots totales combinados.
    → Los slots del Brujo (Magia de Pacto) se calculan **separadamente** y no se mezclan.
  - `get_warlock_slots(warlock_level: int) -> tuple[int, int]`
    → Devuelve `(max_slots, slot_level)` según la tabla de Brujo.
  - `get_max_cantrips(class_slug, class_level, repo) -> int`
  - `get_max_spells_known(class_slug, class_level, repo) -> int | None` (None si prepara)
  - `filter_spells_for_class(class_slug, max_spell_level, repo) -> list[SpellData]`
  - `calculate_spell_save_dc(character, class_slug, repo) -> int`
    → Recibe `class_slug` porque en multiclase cada clase tiene su propia habilidad de lanzador.
  - `calculate_spell_attack_bonus(character, class_slug, repo) -> int`

- [ ] Crear `src/engine/factory.py` con `CharacterFactory` y `CreationContext`:

```python
@dataclass
class CreationContext:
    class_slug: str | None = None
    background_slug: str | None = None
    species_slug: str | None = None
    lineage_slug: str | None = None
    base_ability_scores: dict[str, int] = field(default_factory=dict)
    asi_choices: dict[str, int] = field(default_factory=dict)
    chosen_skills: list[str] = field(default_factory=list)
    equipment_choice_index: int | None = None
    chosen_feats: list[str] = field(default_factory=list)
    character_name: str = ""
```

- [ ] Implementar el flujo de creación en `CharacterFactory.build(ctx, repo)`:
  1. Validar que `ctx` está completo.
  2. Aplicar atributos base + ASI del trasfondo.
  3. Calcular HP nivel 1: `hit_die + CON_mod`.
  4. Recopilar competencias de clase + trasfondo + especie.
  5. Aplicar dote de origen.
  6. Calcular equipamiento inicial.
  7. Calcular conjuros iniciales si la clase es lanzadora.
  8. Devolver `CharacterState` completo.

- [ ] Crear `scripts/test_creation.py`: genera 3 personajes de ejemplo desde consola y los imprime.
- [ ] Tests `tests/test_factory.py`:
  - Crear un Bardo Criminal Elfo con matriz estándar → verificar todos los valores.
  - Crear un Guerrero Soldado Humano → verificar CA con cota de malla.
  - Crear un Mago Erudito Gnomo → verificar DC de conjuro y conjuros conocidos.

### Resultado esperado
Se puede generar un personaje nivel 1 completamente funcional sin abrir la UI.

---

## Fase 4 — Motor de subida de nivel

**Objetivo:** Progresión completa de nivel 1 a 20 con soporte nativo de multiclaseo.

### Principio fundamental: nivel total vs nivel de clase

> Los disparadores de la hoja dependen de **dos contadores distintos** que el motor
> debe tratar de forma estricta e independiente:
>
> | Disparador | Escala con | Ejemplo |
> |---|---|---|
> | Bono de Competencia | **Nivel Total** | PB +3 cuando `total_level == 5` |
> | ASI / Dote | **Nivel de Clase** | ASI al nivel 4 de Bardo, independientemente de cuántos niveles de Guerrero tenga |
> | Subclase | **Nivel de Clase == 3** | Subclase de Bardo al alcanzar el 3.° nivel de Bardo |
> | Rasgos de clase/subclase | **Nivel de Clase** | Los rasgos de tabla del Bardo usan su nivel de Bardo |
> | Slots de conjuro combinados | **Nivel Total ponderado** | Suma de niveles efectivos de todas las clases lanzadoras |
> | Slots del Brujo (Pacto) | **Nivel de Brujo** | Independiente, no se mezclan |

### Tareas

- [ ] Crear `src/engine/progression.py` con `LevelUpEngine`:

```python
class LevelUpEngine:
    def level_up(
        self,
        character: CharacterState,
        choices: LevelUpChoices,
        repo: GameDataRepository
    ) -> CharacterState:
        """
        Aplica una subida de nivel en la clase indicada por choices.target_class_slug.
        Si la clase no existe aún en character.class_levels, la añade (multiclaseo).
        Devuelve un nuevo CharacterState inmutable.
        """
```

- [ ] Definir `LevelUpChoices` con soporte de multiclaseo:

```python
@dataclass
class LevelUpChoices:
    # OBLIGATORIO: en qué clase se aplica el nuevo nivel
    target_class_slug: str
    # True si es una clase NUEVA (multiclaseo); False si ya existe en class_levels
    is_new_class: bool

    # HP
    hp_roll: int | None    # None = usar promedio fijo (floor(hit_die/2) + 1)

    # Subclase — solo requerido si level_in_class(target_class_slug) == 2
    # (es decir, al alcanzar el nivel 3 de esa clase)
    subclass_slug: str | None

    # ASI o Dote — solo si target_class_slug.asi_levels contiene el nivel de clase resultante
    feat_slug: str | None              # None = usar ASI en lugar de dote
    asi_choices: dict[str, int] | None # {"STR": 1, "DEX": 1} si elige ASI

    # Conjuros — listas por clase porque cada clase tiene su propia lista
    new_spells: list[str]       # slugs a aprender
    replaced_spell: str | None  # slug a olvidar (si la clase permite sustitución)
```

- [ ] Lógica de `level_up()` — orden estricto de operaciones:

  1. **Validar `target_class_slug`:**
     - Si `is_new_class=True`: llamar `validate_multiclass_requirements()`. Si falla, lanzar `ValidationError`.
     - Si `is_new_class=False`: verificar que la clase ya existe en `class_levels`.
  2. **Calcular nuevo nivel de clase:**
     - `new_class_level = level_in_class(target_class_slug) + 1`
     - Verificar que `total_level() + 1 <= 20`.
  3. **Añadir HP:**
     - `hp_gained = hp_roll_or_avg + CON_mod` con el dado de golpe de `target_class_slug`.
     - Si `is_new_class=True`: el HP del nivel 1 de la nueva clase es `1 + CON_mod` (se asume máximo para la primera toma). *Ajustar según política de casa.*
  4. **Actualizar `class_levels`:**
     - Si clase nueva: añadir `ClassEntry(class_slug=target, level=1, subclass_slug=None, hit_dice_rolled=[roll])`.
     - Si clase existente: incrementar `entry.level` y hacer `append(roll)` en `hit_dice_rolled`.
  5. **Disparadores de NIVEL DE CLASE** (usar `new_class_level`, no `total_level`):
     - Si `new_class_level == 3`: activar selección de subclase para `target_class_slug`.
     - Si `new_class_level` está en `class_data.asi_levels`: activar ASI o Dote.
     - Activar rasgos de clase y subclase para `new_class_level`.
  6. **Disparadores de NIVEL TOTAL** (usar `total_level()` después del incremento):
     - Si `total_level()` cruza umbral (5, 9, 13, 17): actualizar `proficiency_bonus`.
  7. **Actualizar slots de conjuro (regla multiclase):**
     - Llamar a `spellcasting.calculate_combined_spell_slots(character_updated, repo)`.
     - Reemplazar `spell_slots_max` con el resultado combinado.
     - Si `target_class_slug == 'warlock'`: recalcular también `warlock_slots_max` y `warlock_slot_level`.
  8. **Actualizar conjuros disponibles:**
     - Añadir `new_spells` a `spells_known[target_class_slug]`.
     - Eliminar `replaced_spell` si aplica.
  9. **Aplicar ASI o Dote:**
     - Si `feat_slug` definido: añadir a `feats` y aplicar `asi` del feat a `ability_scores`.
     - Si `asi_choices` definido: aplicar directamente a `ability_scores`.
     - Si cambió CON: llamar retroactividad.

- [ ] Crear `src/engine/retroactivity.py`:
  - `recalculate_hp_for_con_increase(character: CharacterState, old_con_mod: int, new_con_mod: int) -> int`
  - Fórmula: `new_hp_max = old_hp_max + (new_con_mod - old_con_mod) * total_level`
  - **Nota multiclase:** usa `total_level()`, no nivel de una clase.

- [ ] Tests `tests/test_progression.py`:
  - Subir un Bardo monoclase de nivel 1 a 20 → verificar HP, PB y slots en cada paso.
  - Verificar que nivel 3 **de Bardo** activa la selección de subclase.
  - Verificar que nivel 4 **de Bardo** activa ASI, sin importar cuántos niveles tenga de otras clases.
  - Guerrero: verificar ASI extra en niveles **de clase** 6 y 14.
  - **Tests de multiclaseo:**
    - Bardo 3 → añadir Guerrero 1 → `total_level == 4`, PB sigue siendo +2.
    - Bardo 4 → Guerrero 1 → `total_level == 5`, PB sube a +3 (disparado por nivel total).
    - Bardo 4 / Guerrero 1 → verificar que ASI del nivel 4 de Bardo ya fue aplicada, y que el nivel 1 de Guerrero NO dispara ASI.
    - Bardo 2 → añadir clase nueva Guerrero → verificar `validate_multiclass_requirements` con STR 13.
    - Bardo 5 / Mago 5 → slots combinados: nivel efectivo = 5+5=10 → tabla de lanzador nivel 10.
    - Bardo 3 / Brujo 2 → slots de Bardo nivel 3 (combinados) + slots de Pacto nivel 2 de Brujo **separados**.
    - Explorador 4 / Paladín 4 → nivel efectivo = 2 + 2 = 4 (mitad de cada uno).

- [ ] Tests `tests/test_retroactivity.py`:
  - Personaje nivel total 5 CON 14 (+2) sube a CON 16 (+3) → HP sube en +5 (`total_level * delta_mod`).
  - Personaje multiclase Bardo 3 / Guerrero 2 sube CON → HP sube en +5 (usa `total_level == 5`).

### Resultado esperado
El personaje puede subir de nivel, monoclase o multiclase, sin perder consistencia mecánica.

---

## Fase 5 — Fundación de la UI en PySide6

**Objetivo:** Ventana funcional con estilo dark fantasy y pixel art nítido.

### Tareas

- [ ] Crear `src/ui/theme.py`:
  - Paleta oscura: fondo `#0D0D0F`, superficie `#161618`, acento `#C8A96E` (dorado parchment).
  - Texto primario `#E8DCC8`, texto secundario `#8A7A66`.
  - Fuentes: pixel art para títulos, sans-serif para cuerpo.
  - Función `apply_theme(app: QApplication) -> None` que carga el QSS completo.

- [ ] Crear `src/ui/pixel_art.py`:
  - `load_pixmap(path: str, scale: int) -> QPixmap` → siempre `Qt.FastTransformation`.
  - `PixelPainter` context manager que desactiva `SmoothPixmapTransform`.
  - Nunca usar `Qt.SmoothTransformation`.

- [ ] Crear `src/ui/app.py`:
  - `LirielApp(QMainWindow)` con barra de menú, área central y barra de estado.
  - Conectar señal de cierre con guardado de sesión.

- [ ] Crear `src/ui/navigation.py`:
  - `SceneManager` que gestiona un `QStackedWidget` con escenas con nombre.
  - `push_scene(name, scene)`, `go_to(name)`, `go_back()`.

- [ ] Crear widgets base en `src/ui/widgets/`:
  - `PixelButton`: botón con sprite de fondo y hover animado.
  - `PixelLabel`: label con fuente pixel art configurable.
  - `PixelPanel`: panel con borde decorativo y fondo semitransparente.
  - `StatWidget`: muestra una característica (nombre + puntuación + modificador).
  - `SkillWidget`: fila de habilidad con checkbox de competencia y valor.
  - `SpellWidget`: fila de conjuro con nivel, nombre, escuela y botón de info.

- [ ] Crear `src/ui/scenes/main_menu.py`:
  - Botones: Nuevo Personaje, Cargar Personaje, Opciones, Salir.
  - Logo de Liriel centrado con animación de fade-in.

- [ ] Probar navegación: main_menu → (placeholder) → volver.

### Resultado esperado
La app ya se ve como una aplicación real, no un prototipo vacío.

---

## Fase 6 — Wizard de creación (GUI)

**Objetivo:** Crear personajes nivel 1 desde una interfaz guiada, paso a paso.

### Tareas

- [ ] Crear `src/ui/scenes/creation_wizard.py` como `QWizard` o secuencia de pantallas.
- [ ] Implementar los 7 pasos con su pantalla dedicada:

| Paso | Pantalla | Contenido |
|---|---|---|
| 1 | Clase | Lista de clases con descripción, dado de golpe, tipo de lanzador |
| 2 | Trasfondo | Lista de trasfondos, muestra ASI disponibles y dote de origen |
| 3 | Especie | Lista de especies, linajes opcionales, rasgos |
| 4 | Atributos | Selector: Matriz Estándar / Compra de Puntos; asignación de los bonos del trasfondo |
| 5 | Habilidades | Lista filtrada según clase + trasfondo; checkboxes hasta el límite |
| 6 | Equipo | Opciones de equipo de clase + trasfondo; toggle para oro inicial |
| 7 | Resumen | Vista previa de la hoja completa antes de confirmar |

- [ ] Cada paso llama a `CharacterFactory` internamente; bloquea el "Siguiente" si la selección es inválida.
- [ ] El resumen final muestra: HP, CA, iniciativa, salvaciones, habilidades, ataques, conjuros (si aplica).
- [ ] Al confirmar, guarda el personaje con `file_io.save_character()` y navega a la hoja.

### Resultado esperado
El usuario puede crear un personaje completo sin tocar la consola.

---

## Fase 7 — Hoja de personaje (GUI)

**Objetivo:** Pantalla central que muestra y permite editar la hoja completa.

### Tareas

- [ ] Crear `src/ui/scenes/character_sheet.py`.
- [ ] La hoja se divide en secciones con scroll vertical:

| Sección | Contenido |
|---|---|
| Cabecera | Nombre, especie, trasfondo, nivel total; **lista de clases**: `Bardo 4 / Guerrero 1` con subclase de cada una |
| Características | 6 `StatWidget` con puntuación y modificador |
| Combate pasivo | HP (actual/máximo), CA, Iniciativa, Velocidad, Bono de Competencia |
| Salvaciones | 6 filas con modificador total |
| Habilidades | 18 `SkillWidget` con pericia/experiencia marcada |
| Rasgos | Lista de rasgos activos de **cada clase y subclase**, especie y dotes; agrupados por origen |
| Conjuros | Pool de slots combinados (si hay ≥1 lanzador) + slots de Pacto (si hay Brujo); lista de conjuros por clase |
| Equipo | Lista de inventario con peso total; botón de equipar/quitar |

- [ ] Botón **Guardar** → `file_io.save_character()`.
- [ ] Botón **Subir de Nivel** → navega a `level_up_scene`.
- [ ] Botón **Gestionar Equipo** → navega a `inventory_scene`.
- [ ] Todos los valores se leen de `CharacterState`; ningún valor se calcula en la UI.
- [ ] Si el personaje cambia, emitir señal `character_updated` y refrescar todos los widgets.

### Resultado esperado
La hoja funciona como pantalla central de la aplicación.

---

## Fase 8 — Level Up (GUI)

**Objetivo:** Subir de nivel desde la interfaz con todas las decisiones requeridas, incluyendo multiclaseo.

### Tareas

- [ ] Crear `src/ui/scenes/level_up_scene.py`.
- [ ] El flujo de pantallas es secuencial. **El primer paso siempre es la selección de clase:**

#### Paso 1 — Selección de clase (SIEMPRE el primer paso)

- [ ] Mostrar dos opciones exclusivas:
  - **Avanzar en una clase actual:** lista de `ClassEntry` del personaje con su nivel actual.
  - **Adoptar una nueva clase (multiclaseo):** lista de clases disponibles en el repositorio.
    - Cada clase muestra sus `multiclass_requirements`. Las que el personaje NO cumple aparecen en gris y deshabilitadas.
    - Al pasar el cursor sobre una clase deshabilitada, mostrar tooltip: *"Requiere [Característica] [valor]"*.
    - Si `total_level() == 20`: deshabilitar la opción de nueva clase completamente.
- [ ] El usuario selecciona `target_class_slug` e `is_new_class`. Esto determina todos los pasos siguientes.

#### Pasos siguientes — Condicionales según clase elegida

| Decisión | Condición |
|---|---|
| HP: tirar dado vs promedio | **Siempre** (dado de golpe de `target_class_slug`) |
| Seleccionar subclase | Solo cuando `level_in_class(target) == 2` (→ alcanza nivel 3 de clase) |
| Seleccionar Dote o ASI | Solo cuando `new_class_level` está en `class_data.asi_levels` |
| Aprender conjuros nuevos | Si `target_class_slug` es una clase lanzadora |
| Reemplazar un conjuro | Si `target_class_slug` permite sustitución en su tabla |
| Info: PB aumenta | Si `total_level() + 1` cruza umbral (5, 9, 13, 17) — informativo |

- [ ] Panel lateral permanente durante todo el flujo: **Vista previa de la hoja** actualizada en tiempo real:
  - Nivel total: `4 → 5`
  - Desglose de clases: `Bardo 4 / Guerrero 0 → Bardo 4 / Guerrero 1`
  - HP máximo: `antes → después`
  - Bono de Competencia: `+2 → +3` (resaltado si cambia)
  - Slots de conjuro: tabla combinada antes/después
  - Slots de Pacto: si hay Brujo
- [ ] Al confirmar, construir `LevelUpChoices` con todos los campos y llamar `LevelUpEngine.level_up()` → actualizar `CharacterState` → guardar → volver a la hoja.
- [ ] Si el ASI aumenta CON: mostrar aviso de retroactividad con preview del nuevo HP máximo antes de confirmar.

### Resultado esperado
El level up en la UI replica exactamente la lógica del motor, para personajes monoclase y multiclase.

---

## Fase 9 — Inventario y equipo (GUI)

**Objetivo:** Gestionar equipo y ver su impacto mecánico en la hoja.

### Tareas

- [ ] Crear `src/ui/scenes/inventory_scene.py`.
- [ ] Panel izquierdo: inventario actual con peso total y capacidad (FUE × 15 libras).
- [ ] Panel derecho: catálogo de equipo del repositorio con búsqueda y filtro por categoría.
- [ ] Acciones disponibles:
  - Equipar armadura → recalcula CA → refresca hoja.
  - Equipar/quitar escudo → recalcula CA.
  - Añadir/quitar armas del inventario → recalcula ataques visibles en la hoja.
  - Añadir objetos genéricos (herramientas, consumibles).
- [ ] Ningún cálculo de CA o ataque se hace en la escena; todo pasa por `combat.py`.

### Resultado esperado
El equipo impacta de forma visible e inmediata en la hoja.

---

## Fase 10 — Assets y pulido visual

**Objetivo:** Dar identidad artística coherente a la app.

### Recursos a crear (Aseprite)

- [ ] Iconos de clase (12 iconos, 32×32 px).
- [ ] Iconos de habilidad (18 iconos, 16×16 px).
- [ ] Iconos de escuela de magia (8 iconos, 16×16 px).
- [ ] Sprites de UI: botones, paneles, bordes decorativos, scroll.
- [ ] Fondo de pantalla para main menu (dark fantasy, estático o animado en loop).
- [ ] Fuente pixel art personalizada (o selección de fuente libre estilo fantasy).

### Pulido de UI

- [ ] Animaciones de hover en botones (escala ligera o brillo).
- [ ] Transición de fade entre escenas (150ms).
- [ ] Tooltips en todos los rasgos, habilidades y conjuros.
- [ ] Scroll suave en la hoja de personaje.
- [ ] Soporte de teclado: Tab entre campos, Enter para confirmar.

### Resultado esperado
La app tiene coherencia visual y pixel art nítido sin interpolación.

---

## Fase 11 — QA y empaquetado

**Objetivo:** Versión distribuible y estable.

### Tests de integración

- [ ] Crear personaje completo de cada clase → guardar → cargar → verificar valores idénticos.
- [ ] Subir cada clase de nivel 1 a 20 → verificar HP, PB, slots, rasgos en cada paso.
- [ ] Verificar retroactividad CON en nivel 4 para cada clase.
- [ ] Probar clases no lanzadoras (Guerrero, Bárbaro): sin sección de conjuros.
- [ ] Probar clases half-caster (Paladín, Explorador): slots reducidos.
- [ ] Probar Brujo: slots cortos (`short rest`), máximo nivel 5.

### Empaquetado

- [ ] Probar `pyinstaller main.py --onefile --windowed --name Liriel`.
- [ ] Verificar que los JSON de `data/` se empaquetan con `--add-data`.
- [ ] Verificar que los assets se empaquetan.
- [ ] Probar el ejecutable en una máquina Windows sin Python instalado.

### Resultado esperado
Versión 1.0 utilizable por terceros como ejecutable independiente.

---

## Apéndice — Renderizado pixel art en PySide6

**Regla absoluta:** nunca usar `Qt.SmoothTransformation`.

```python
# Al cargar un pixmap y escalarlo
pixmap = QPixmap(path).scaled(w, h, Qt.KeepAspectRatio, Qt.FastTransformation)

# En cualquier paintEvent personalizado
def paintEvent(self, event):
    painter = QPainter(self)
    painter.setRenderHint(QPainter.SmoothPixmapTransform, False)
    painter.drawPixmap(rect, self.pixmap)
```

**Por qué:** `SmoothTransformation` difumina los píxeles del sprite art, destruyendo la estética.
`FastTransformation` = escalado por vecino más cercano = píxeles nítidos.

---

## Apéndice — Fórmulas de D&D 5.5e implementadas por el motor

### Fórmulas generales

| Valor | Fórmula |
|---|---|
| Modificador de característica | `⌊(puntuación − 10) / 2⌋` |
| Nivel total | `sum(entry.level for entry in class_levels)` |
| Bono de competencia | Nivel total 1-4: +2 / 5-8: +3 / 9-12: +4 / 13-16: +5 / 17-20: +6 |
| HP nivel 1 (clase inicial) | `hit_die + CON_mod` |
| HP niveles 2+ | `HP_prev + ⌊hit_die/2⌋ + 1 + CON_mod` (promedio) ó `roll + CON_mod` |
| HP retroactivo por CON | `HP_max += (new_CON_mod − old_CON_mod) × total_level` |
| CA sin armadura | `10 + DEX_mod` |
| CA armadura ligera | `base_ac + DEX_mod` |
| CA armadura media | `base_ac + min(DEX_mod, 2)` |
| CA armadura pesada | `base_ac` |
| Escudo | `+2 a cualquier CA` |
| Iniciativa | `DEX_mod` |
| Salvación competente | `ability_mod + PB` |
| Salvación sin competencia | `ability_mod` |
| Tirada de ataque de conjuro | `ability_mod_lanzador + PB` |
| CD de salvación de conjuro | `8 + ability_mod_lanzador + PB` |
| Bono de ataque cuerpo a cuerpo | `STR_mod + PB` (o `DEX_mod + PB` si finesse) |
| Bono de ataque a distancia | `DEX_mod + PB` |
| Daño cuerpo a cuerpo | `dado_arma + STR_mod` (o `DEX_mod` si finesse) |
| Daño a distancia | `dado_arma + DEX_mod` |

### Fórmulas de multiclaseo — Slots de conjuro combinados

> Fuente: regla de multiclaseo de D&D 5.5e 2024, PHB p. 230.

| Tipo de lanzador | Nivel efectivo por nivel de clase |
|---|---|
| Lanzador completo (Bardo, Clérigo, Druida, Mago, Hechicero) | `class_level × 1` |
| Medio lanzador (Explorador, Paladín) | `floor(class_level × 0.5)` |
| Tercio lanzador (Guerrero Caballero Arcano, Pícaro Embaucador) | `floor(class_level × 0.333)` solo si subclase activa |
| Brujo | **No se suma**. Sus slots son independientes (Magia de Pacto) |
| No lanzador | `0` |

**Cálculo:**
```
nivel_efectivo_total = sum(get_single_class_caster_level(class_slug, level))
combined_slots = tabla_de_lanzador_completo[floor(nivel_efectivo_total)]
```

**Ejemplo 1:** Bardo 3 / Mago 4
```
Nivel efectivo = 3 + 4 = 7
Slots = tabla nivel 7 → 4×1, 3×2, 3×3, 1×4
```

**Ejemplo 2:** Paladín 5 / Explorador 6
```
Nivel efectivo = floor(5/2) + floor(6/2) = 2 + 3 = 5
Slots = tabla nivel 5 → 4×1, 3×2, 2×3
```

**Ejemplo 3:** Bardo 4 / Brujo 3
```
Nivel efectivo combinado = 4 (Bardo completo; Brujo no cuenta)
Slots combinados = tabla nivel 4 → 4×1, 3×2
Slots de Pacto del Brujo = 2 slots de nivel 2 (tabla de Brujo nivel 3, independientes)
```

### Disparadores: nivel de clase vs nivel total

| Disparador | Variable correcta |
|---|---|
| Bono de Competencia | `total_level()` |
| ASI / Dote | `level_in_class(class_slug)` comparado con `class_data.asi_levels` |
| Selección de subclase | `level_in_class(class_slug) == 3` |
| Rasgos de clase y subclase | `level_in_class(class_slug)` |
| Slots combinados | `floor(sum de niveles efectivos)` |
| Slots de Pacto (Brujo) | `level_in_class('warlock')` |
