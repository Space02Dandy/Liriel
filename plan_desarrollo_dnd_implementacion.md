# Plan de Implementacion de Liriel

## Objetivo
Construir una aplicacion de escritorio gratuita y open-source para gestionar hojas de personaje completas de D&D 5.5e usando **Python + PySide6** y assets de pixel art propios.

## Decision tecnica principal

- **GUI:** PySide6
- **Renderizado pixel art:** `Qt.FastTransformation` y pintado manual con `QPainter`
- **Logica de reglas:** capa separada sin dependencia de Qt
- **Datos:** JSON locales
- **Persistencia de personajes:** JSON propio `.liriel`

## Estructura recomendada del proyecto

```
Liriel/
├── main.py
├── requirements.txt
├── data/
├── assets/
├── src/
│   ├── data/
│   ├── engine/
│   ├── ui/
│   └── utils/
├── tests/
└── characters/
```

## Reglas de arquitectura

- La UI nunca debe calcular reglas de D&D.
- El motor nunca debe importar PySide6.
- Todos los datos del juego vienen de JSON.
- Cada cambio de personaje debe pasar por el motor y luego refrescar la UI.
- Cualquier calculo derivado debe ser reproducible y testeable.

---

## Fase 0. Preparacion del proyecto

### Objetivo
Dejar el repositorio listo para trabajar sin bloqueos.

- [ ] Crear `requirements.txt` con `PySide6`, `pytest`, `pyinstaller` y utilidades necesarias.
- [ ] Crear la estructura de carpetas completa del proyecto.
- [ ] Crear `main.py` minimo que solo arranque la app y abra una ventana vacia.
- [ ] Crear `src/__init__.py`, `src/data/__init__.py`, `src/engine/__init__.py`, `src/ui/__init__.py`, `src/utils/__init__.py`.
- [ ] Crear `.gitignore` para `__pycache__`, `.venv`, `build`, `dist`, `characters` y archivos temporales de PyCharm.
- [ ] Crear `tests/test_smoke.py` para verificar que el entorno de pruebas funciona.

### Resultado esperado
El proyecto abre y el entorno ejecuta tests sin fallar.

---

## Fase 1. Base de datos JSON y cargador

### Objetivo
Poder leer todas las reglas del juego desde archivos estaticos.

- [ ] Crear `src/engine/enums.py` con las enumeraciones base: abilities, skills, schools, armor categories, feat types, sizes y damage types.
- [ ] Crear `src/data/models.py` con dataclasses para clases, subclases, especies, trasfondos, conjuros, dotes, armas, armaduras y equipo.
- [ ] Crear `src/data/loader.py` con funciones de carga por archivo:
  - `load_classes()`
  - `load_subclasses()`
  - `load_species()`
  - `load_backgrounds()`
  - `load_spells()`
  - `load_feats()`
  - `load_weapons()`
  - `load_armor()`
  - `load_equipment()`
- [ ] Crear `src/data/repository.py` con un repositorio unico para consultar por `slug`.
- [ ] Crear el contenido inicial de `data/classes.json`.
- [ ] Crear el contenido inicial de `data/subclasses.json`.
- [ ] Crear el contenido inicial de `data/species.json`.
- [ ] Crear el contenido inicial de `data/backgrounds.json`.
- [ ] Crear el contenido inicial de `data/spells.json`.
- [ ] Crear el contenido inicial de `data/feats.json`.
- [ ] Crear el contenido inicial de `data/weapons.json`.
- [ ] Crear el contenido inicial de `data/armor.json`.
- [ ] Crear el contenido inicial de `data/equipment.json`.
- [ ] Escribir tests de validacion de carga en `tests/test_loader.py`.
- [ ] Escribir tests de referencias cruzadas entre archivos.

### Orden exacto de trabajo en esta fase

1. Crear `enums.py`.
2. Crear `models.py`.
3. Crear `loader.py`.
4. Crear `repository.py`.
5. Escribir los JSON minimos funcionales.
6. Validar con tests.

### Resultado esperado
El proyecto puede arrancar, cargar datos y detectar errores de contenido.

---

## Fase 2. Modelo de personaje

### Objetivo
Definir el objeto central que representa una hoja de personaje.

- [ ] Crear `src/engine/character.py` con `CharacterState`.
- [ ] Definir atributos basicos: nombre, clase, subclase, especie, trasfondo, nivel, atributos, HP, AC, iniciativa, velocidad, salvaciones, habilidades, equipo, conjuros y dotes.
- [ ] Implementar propiedades calculadas para modificadores de atributo.
- [ ] Implementar `to_dict()` y `from_dict()` para guardar/cargar.
- [ ] Crear `src/utils/file_io.py` para persistencia `.liriel`.
- [ ] Crear tests de serializacion y deserializacion.

### Resultado esperado
Un personaje puede existir en memoria, serializarse y recuperarse intacto.

---

## Fase 3. Motor de creacion Nivel 1

### Objetivo
Construir un personaje completo sin interfaz, solo con motor Python.

- [ ] Crear `src/engine/validation.py` para validar elecciones.
- [ ] Crear `src/engine/combat.py` para CA, ataques, daño e iniciativa.
- [ ] Crear `src/engine/spellcasting.py` para slots, trucos, conjuros conocidos y preparados.
- [ ] Crear `src/engine/factory.py` con `CharacterFactory`.
- [ ] Crear `CreationContext` para llevar el estado paso a paso.
- [ ] Implementar el flujo de creacion en este orden:
  - [ ] seleccionar clase
  - [ ] seleccionar trasfondo
  - [ ] seleccionar especie
  - [ ] asignar atributos
  - [ ] elegir habilidades
  - [ ] elegir equipo
  - [ ] finalizar personaje
- [ ] Calcular HP inicial, bono de competencia, CA, iniciativa, salvaciones, competencias y conjuros iniciales.
- [ ] Escribir `scripts/test_creation.py` para generar personajes de ejemplo desde consola.
- [ ] Escribir tests de nivel 1 en `tests/test_factory.py`.

### Resultado esperado
Se puede generar un personaje de nivel 1 completamente funcional sin UI.

---

## Fase 4. Motor de subida de nivel

### Objetivo
Permitir progresion completa de nivel 1 a 20.

- [ ] Crear `src/engine/progression.py` con `LevelUpEngine`.
- [ ] Crear `src/engine/retroactivity.py` para recalculo retroactivo de HP por CON.
- [ ] Hacer que cada subida de nivel haga lo siguiente:
  - [ ] sumar HP
  - [ ] actualizar bono de competencia si corresponde
  - [ ] activar seleccion de subclase en nivel 3
  - [ ] activar seleccion de dote o ASI en niveles correspondientes
  - [ ] actualizar espacios de conjuro
  - [ ] permitir aprender o reemplazar conjuros
  - [ ] actualizar rasgos de clase y subclase
- [ ] Manejar el caso de CON que sube y recalcula HP retroactivo.
- [ ] Escribir tests de progresion en `tests/test_progression.py`.
- [ ] Escribir tests especificos de retroactividad en `tests/test_retroactivity.py`.

### Orden exacto de trabajo en esta fase

1. Crear `progression.py`.
2. Crear `retroactivity.py`.
3. Conectar con `character.py`.
4. Conectar con `spellcasting.py`.
5. Escribir tests.

### Resultado esperado
El personaje puede subir de nivel sin perder consistencia mecanica.

---

## Fase 5. Fundacion de la UI en PySide6

### Objetivo
Arrancar una ventana funcional con estilo dark fantasy y pixel art nitido.

- [ ] Crear `src/ui/app.py` con `QApplication`, `QMainWindow` y gestion basica de escenas.
- [ ] Crear `src/ui/theme.py` con paleta oscura, fuentes y QSS.
- [ ] Crear `src/ui/pixel_art.py` con utilidades para cargar y escalar pixmaps sin suavizado.
- [ ] Crear `src/ui/navigation.py` para navegar entre pantallas.
- [ ] Crear widgets base:
  - [ ] `pixel_label.py`
  - [ ] `pixel_button.py`
  - [ ] `pixel_panel.py`
  - [ ] `stat_widget.py`
  - [ ] `skill_widget.py`
  - [ ] `spell_widget.py`
- [ ] Crear `src/ui/scenes/main_menu.py`.
- [ ] Probar que la ventana abre, muestra menu principal y navega.

### Resultado esperado
La aplicacion ya se ve como una app real y no como un prototipo vacio.

---

## Fase 6. Wizard de creacion GUI

### Objetivo
Crear personajes desde una interfaz guiada.

- [ ] Crear `src/ui/scenes/creation_wizard.py`.
- [ ] Dividirlo en pasos claros:
  - [ ] clase
  - [ ] trasfondo
  - [ ] especie
  - [ ] atributos
  - [ ] habilidades
  - [ ] equipo
  - [ ] resumen final
- [ ] Conectar cada paso con `CharacterFactory`.
- [ ] Bloquear opciones invalidas segun reglas.
- [ ] Mostrar vista previa del personaje en cada paso.
- [ ] Guardar el personaje al confirmar el resumen.

### Resultado esperado
El usuario puede crear un personaje completo sin tocar consola.

---

## Fase 7. Hoja de personaje

### Objetivo
Mostrar y editar la hoja completa de forma clara.

- [ ] Crear `src/ui/scenes/character_sheet.py`.
- [ ] Mostrar cabecera, atributos, HP, CA, salvaciones, habilidades, equipo, rasgos y conjuros.
- [ ] Hacer la hoja desplazable.
- [ ] Conectar botones de guardar, subir de nivel y gestionar equipo.
- [ ] Refrescar datos desde `CharacterState` cuando cambie algo.

### Resultado esperado
La hoja funciona como pantalla central de la aplicacion.

---

## Fase 8. Level Up GUI

### Objetivo
Subir de nivel desde la interfaz con todas las decisiones.

- [ ] Crear `src/ui/scenes/level_up_scene.py`.
- [ ] Mostrar el aumento de HP.
- [ ] Mostrar la subclase en nivel 3.
- [ ] Mostrar la dote o ASI en niveles correctos.
- [ ] Mostrar nuevos conjuros y reemplazos.
- [ ] Integrar la retroactividad de CON con preview antes de confirmar.

### Resultado esperado
El level up de la UI replica la logica del motor.

---

## Fase 9. Inventario y equipo

### Objetivo
Gestionar equipo y su impacto mecanico.

- [ ] Crear `src/ui/scenes/inventory_scene.py`.
- [ ] Permitir equipar, quitar y comparar objetos.
- [ ] Recalcular CA, ataques y carga al cambiar equipo.

### Resultado esperado
El equipo impacta de forma visible en la hoja.

---

## Fase 10. Assets y pulido visual

### Objetivo
Dar identidad artistica a la app.

- [ ] Crear sprites de UI en Aseprite.
- [ ] Crear iconos de clases, stats, habilidades y conjuros.
- [ ] Crear fuentes pixel-art legibles.
- [ ] Crear paneles y botones con estilo dark fantasy.
- [ ] Ajustar escalado para que no haya interpolacion.

### Resultado esperado
La app tiene coherencia visual y pixel art nitido.

---

## Fase 11. QA y empaquetado

### Objetivo
Dejar una version distribuible.

- [ ] Crear tests de integracion completos.
- [ ] Probar crear, guardar, cargar y subir personajes hasta nivel 20.
- [ ] Verificar clases magicas y no magicas.
- [ ] Empaquetar con PyInstaller.
- [ ] Probar el ejecutable en una maquina limpia.

### Resultado esperado
Version utilizable para terceros.

---

## Renderizado pixel art en PySide6

Usar siempre `Qt.FastTransformation` al escalar:

```python
pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.FastTransformation)
```

En `paintEvent`:

```python
painter.setRenderHint(QPainter.SmoothPixmapTransform, False)
```

No usar `Qt.SmoothTransformation`.

---

## Orden recomendado real de implementacion

1. `enums.py`
2. `models.py`
3. `loader.py`
4. `repository.py`
5. JSON minimos funcionales
6. `character.py`
7. `combat.py`
8. `spellcasting.py`
9. `factory.py`
10. `progression.py`
11. `retroactivity.py`
12. `file_io.py`
13. `pixel_art.py`
14. `app.py`
15. `main_menu.py`
16. `creation_wizard.py`
17. `character_sheet.py`
18. `level_up_scene.py`
19. `inventory_scene.py`
20. assets finales
21. tests de integracion
22. empaquetado
