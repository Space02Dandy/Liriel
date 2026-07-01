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
│   ├── classes.json
│   ├── subclasses.json
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
- [ ] `data/subclasses.json` — 2-3 subclases por clase (las del SRD 2024).
- [ ] `data/species.json` — Humano, Elfo, Enano, Halfling, Gnomo, Semiorco, Tiefling, Draconiano.
- [ ] `data/backgrounds.json` — Al menos 10 trasfondos del manual básico 2024.
- [ ] `data/feats.json` — Todas las dotes de origen + dotes generales del SRD.
- [ ] `data/weapons.json` — Todas las armas simples y marciales del SRD.
- [ ] `data/armor.json` — Todas las armaduras y escudo del SRD.
- [ ] `data/equipment.json` — Paquetes de clase, herramientas, equipo básico.
- [ ] `data/spells.json` — Conjuros del SRD niveles 0-9 (mínimo 50 conjuros representativos por escuela).

### Tareas — Tests

- [ ] `tests/test_loader.py`:
  - Verificar que todos los JSON cargan sin excepción.
  - Verificar que el recuento de objetos es correcto (≥ N por tipo).
  - Verificar slugs únicos.
- [ ] `tests/test_loader.py` — tests de referencias cruzadas:
  - `class_slug` de subclases existe en clases.
  - `origin_feat_slug` de trasfondos existe en dotes.
  - Clases en `spells.json` existen en `classes.json`.

### Resultado esperado
El proyecto arranca, carga datos y detecta cualquier error de contenido antes de mostrar UI.

---

## Fase 2 — Modelo de personaje

**Objetivo:** Objeto central `CharacterState` que representa una hoja de personaje completa.

### Tareas

- [ ] Crear `src/engine/character.py` con `CharacterState`:

```python
@dataclass
class CharacterState:
    # Identidad
    name: str
    class_slug: str
    subclass_slug: str | None
    species_slug: str
    lineage_slug: str | None
    background_slug: str
    level: int

    # Puntuaciones de característica (base + ASI acumulado)
    ability_scores: dict[str, int]   # {"STR": 16, "DEX": 14, ...}

    # Salud
    hp_max: int
    hp_current: int
    hp_temp: int
    hit_dice_used: int

    # Equipo activo
    armor_slug: str | None
    shield_equipped: bool
    weapons: list[str]               # slugs equipados
    inventory: list[dict]            # {"slug": str, "qty": int}

    # Conjuros
    spells_known: list[str]          # slugs
    spells_prepared: list[str]       # slugs (clases que preparan)
    spell_slots_used: dict[str, int] # {"1": N_usados, "2": N_usados, ...}

    # Opciones acumuladas
    skill_proficiencies: list[str]
    tool_proficiencies: list[str]
    saving_throw_proficiencies: list[str]
    feats: list[str]                 # slugs de dotes tomadas

    # Metadatos
    xp: int
    created_at: str                  # ISO 8601
    updated_at: str
```

- [ ] Implementar **propiedades calculadas** (no almacenadas):
  - `ability_modifier(ability: str) -> int` → `floor((score - 10) / 2)`
  - `proficiency_bonus() -> int` → según nivel total
  - `initiative() -> int` → modificador DEX
  - `ac() -> int` → según armadura equipada + DEX + escudo
  - `spell_save_dc(ability: str) -> int` → `8 + PB + mod`
  - `spell_attack_bonus(ability: str) -> int` → `PB + mod`
  - `saving_throw(ability: str) -> int` → mod + PB si competente
  - `skill_bonus(skill: str) -> int` → mod + PB si competente
  - `weapon_attack_bonus(weapon_slug: str) -> int`
  - `weapon_damage_bonus(weapon_slug: str) -> int`

- [ ] Implementar `to_dict() -> dict` y `from_dict(d: dict) -> CharacterState`.
- [ ] Crear `src/utils/file_io.py`:
  - `save_character(character: CharacterState, path: Path) -> None`
  - `load_character(path: Path) -> CharacterState`
  - Formato: JSON con extensión `.liriel`
- [ ] Tests de serialización: un personaje guardado y recargado debe ser idéntico.
- [ ] Tests de propiedades calculadas con valores conocidos.

### Resultado esperado
Un personaje puede existir en memoria, serializar a disco y recuperarse intacto.

---

## Fase 3 — Motor de creación (Nivel 1)

**Objetivo:** Construir un personaje nivel 1 completamente funcional solo con motor Python.

### Tareas

- [ ] Crear `src/engine/validation.py`:
  - `validate_skill_choices(class_slug, chosen_skills, repo) -> bool`
  - `validate_asi_choices(background_slug, chosen_abilities, repo) -> bool`
  - `validate_equipment_choice(class_slug, choice_index, repo) -> bool`
  - `validate_feat_prerequisites(feat_slug, character, repo) -> bool`

- [ ] Crear `src/engine/combat.py` (solo cálculos pasivos para la hoja):
  - `calculate_ac(character: CharacterState, repo: GameDataRepository) -> int`
  - `calculate_initiative(character: CharacterState) -> int`
  - `calculate_weapon_attack(character, weapon_slug, repo) -> tuple[int, str]`
    → devuelve (bono_total, cadena_daño) ej: `(+5, "1d8+3")`

- [ ] Crear `src/engine/spellcasting.py`:
  - `get_available_slots(class_slug, level, repo) -> dict[str, int]`
  - `get_max_cantrips(class_slug, level, repo) -> int`
  - `get_max_spells_known(class_slug, level, repo) -> int | None` (None si prepara)
  - `filter_spells_for_class(class_slug, max_spell_level, repo) -> list[SpellData]`
  - `calculate_spell_save_dc(character, repo) -> int`
  - `calculate_spell_attack_bonus(character, repo) -> int`

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

**Objetivo:** Progresión completa de nivel 1 a 20 con todas las reglas.

### Tareas

- [ ] Crear `src/engine/progression.py` con `LevelUpEngine`:

```python
class LevelUpEngine:
    def level_up(self, character: CharacterState, choices: LevelUpChoices, repo) -> CharacterState:
        """Aplica una subida de nivel y devuelve el nuevo CharacterState."""
```

- [ ] `LevelUpChoices` debe contemplar:
  - `hp_roll: int | None` → None = usar promedio fijo
  - `subclass_slug: str | None` → requerido si nivel == 3
  - `feat_slug: str | None` → si es nivel de ASI/Dote
  - `asi_choices: dict[str, int] | None` → si elige ASI en lugar de dote
  - `new_spells: list[str]` → slugs de conjuros aprendidos
  - `replaced_spell: str | None` → slug del conjuro olvidado

- [ ] Lógica de `level_up()`:
  1. Incrementar `character.level`.
  2. Calcular nuevo HP: `hp_roll_or_avg + CON_mod` y añadir al máximo.
  3. Si nivel 3: aplicar subclase.
  4. Si nivel es ASI/Dote: aplicar feat o ASI (y llamar retroactividad si sube CON).
  5. Si nivel aumenta el bono de competencia: recalcular todas las competencias.
  6. Actualizar slots de conjuro según la tabla de la clase.
  7. Añadir conjuros aprendidos, eliminar el reemplazado si aplica.
  8. Activar nuevos rasgos de clase y subclase para ese nivel.

- [ ] Crear `src/engine/retroactivity.py`:
  - `recalculate_hp_for_con_increase(character: CharacterState, old_con_mod: int, new_con_mod: int) -> int`
  - Fórmula: `new_hp_max = old_hp_max + (new_con_mod - old_con_mod) * level`

- [ ] Tests `tests/test_progression.py`:
  - Subir un Bardo de nivel 1 a 20, verificar HP, PB y slots en cada paso.
  - Verificar que nivel 3 activa la selección de subclase.
  - Verificar que nivel 4, 8, 12, 16, 19 activan ASI/Dote.
  - Guerrero: verificar ASI extra en niveles 6, 14.

- [ ] Tests `tests/test_retroactivity.py`:
  - Personaje nivel 5 CON 14 (+2) sube a CON 16 (+3) → HP debe subir en +5.
  - Personaje nivel 10 sube CON en 2 puntos → HP sube en +10.

### Resultado esperado
El personaje puede subir de nivel sin perder consistencia mecánica.

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
| Cabecera | Nombre, clase/subclase, especie, trasfondo, nivel |
| Características | 6 `StatWidget` con puntuación y modificador |
| Combate pasivo | HP (actual/máximo), CA, Iniciativa, Velocidad, Bono de Competencia |
| Salvaciones | 6 filas con modificador total |
| Habilidades | 18 `SkillWidget` con pericia/experiencia marcada |
| Rasgos | Lista de rasgos activos de clase, subclase, especie y dotes |
| Conjuros | Tabla de slots disponibles/usados + lista de conjuros conocidos/preparados |
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

**Objetivo:** Subir de nivel desde la interfaz con todas las decisiones requeridas.

### Tareas

- [ ] Crear `src/ui/scenes/level_up_scene.py`.
- [ ] Construir el flujo de decisiones según el nivel destino:

| Decisión | Cuándo aparece |
|---|---|
| HP: tirar dado vs promedio | Siempre |
| Seleccionar subclase | Solo cuando nivel destino == 3 |
| Seleccionar Dote o ASI | Niveles ASI de la clase (4, 8, 12, 16, 19 para mayoría) |
| Aprender conjuros nuevos | Si la clase es lanzadora |
| Reemplazar un conjuro | Si la clase permite sustitución |

- [ ] Vista de preview antes de confirmar: muestra el antes/después de HP, PB, slots, atributos.
- [ ] Al confirmar, llama `LevelUpEngine.level_up()` → actualiza `CharacterState` → guarda → vuelve a la hoja.
- [ ] Si el ASI aumenta CON: mostrar aviso de retroactividad con preview del nuevo HP máximo.

### Resultado esperado
El level up en la UI replica exactamente la lógica del motor.

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

| Valor | Fórmula |
|---|---|
| Modificador de característica | `⌊(puntuación − 10) / 2⌋` |
| Bono de competencia | Niveles 1-4: +2 / 5-8: +3 / 9-12: +4 / 13-16: +5 / 17-20: +6 |
| HP nivel 1 | `hit_die + CON_mod` |
| HP niveles 2+ | `HP_prev + ⌊hit_die/2⌋ + 1 + CON_mod` (promedio) ó `roll + CON_mod` |
| HP retroactivo por CON | `HP_max += (new_CON_mod − old_CON_mod) × level` |
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
