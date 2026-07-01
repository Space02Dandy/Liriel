# Plan de Desarrollo de Liriel — Índice

## ¿Qué es Liriel?

Liriel es **única y exclusivamente** un **Constructor y Gestor de Hojas de Personaje** para D&D 5.5e (Revisión 2024).

### Lo que Liriel SÍ hace
- Guiar al usuario por el flujo de creación de personaje (clase → trasfondo → especie → atributos → habilidades → equipo).
- Calcular automáticamente todos los valores derivados: modificadores, CA, HP, bono de competencia, CD de conjuros, tiradas de ataque de conjuro, salvaciones y bono de iniciativa.
- Gestionar la progresión de nivel 1 a 20 (HP, competencias, subclase en nivel 3, ASI/Dotes, slots de conjuro).
- Recalcular HP retroactivamente cuando sube el modificador de Constitución (regla 2024).
- Mostrar y editar la hoja completa de forma visual.
- Guardar y cargar personajes en formato `.liriel` (JSON propio).
- Gestionar inventario e impacto mecánico del equipo equipado (CA, peso, propiedades).
- Filtrar y mostrar la lista de conjuros conocidos/preparados según la clase y el nivel.

### Lo que Liriel NO es y NO hace
| Fuera de alcance | Razón |
|---|---|
| Virtual Tabletop (VTT) | No hay tablero ni movimiento de fichas |
| Simulador de combate | No resuelve turnos, ataques contra enemigos, ni estados |
| Tirador de dados interactivo | No hay widget de dados |
| Sistema de campaña/aventura | No gestiona sesiones, XP ganado por encuentros, ni mapas |
| Chat IA de narración | No genera texto de historia |

---

## Documentación dividida

| Archivo | Contenido |
|---|---|
| [`plan_desarrollo_dnd_json.md`](plan_desarrollo_dnd_json.md) | Estructura detallada de todos los archivos JSON de reglas: esquemas, campos, ejemplos y política de validación. |
| [`plan_desarrollo_dnd_implementacion.md`](plan_desarrollo_dnd_implementacion.md) | Hoja de ruta completa para construir la app fase a fase, con tareas concretas, orden de implementación y criterios de validación. |

---

## Stack tecnológico (resumen rápido)

| Capa | Tecnología |
|---|---|
| GUI | PySide6 |
| Lógica de reglas | Python puro (sin dependencia de Qt) |
| Datos de juego | JSON locales en `data/` |
| Persistencia | JSON propio `.liriel` en `characters/` |
| Tests | pytest + pytest-qt |
| Distribución | PyInstaller |

---

## Estado actual del proyecto

- `main.py` funcional: abre ventana PySide6 vacía. ✅
- `requirements.txt` con PySide6, pytest, pytest-qt, pyinstaller. ✅
- Estructura de carpetas `src/data`, `src/engine`, `src/ui`, `src/utils` creada. ✅
- `data/` vacío: los JSON de reglas aún no existen. ⬜
- Motor de reglas: no implementado. ⬜
- UI de creación y hoja: no implementada. ⬜

**Próxima acción:** Fase 1 — Crear enums, modelos y JSON mínimos funcionales.

---

## Referencia de reglas

El archivo [`Referencia_Reglas_DnD5.5_IA.md`](Referencia_Reglas_DnD5.5_IA.md) contiene todas las fórmulas y reglas estructurales que el motor debe implementar.
