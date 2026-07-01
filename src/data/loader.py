import json
from pathlib import Path
from typing import Any

from .models import (
    ClassData, SubclassData, SpeciesData, BackgroundData,
    FeatData, SpellData, WeaponData, ArmorData, EquipmentData
)

# ─────────────────────────────────────────────────────────────────────────────
# Directorio raíz de datos (relativo al directorio de trabajo del proyecto).
# ─────────────────────────────────────────────────────────────────────────────
_DATA_ROOT = Path("data")


class DataIntegrityError(Exception):
    """Excepción lanzada cuando los datos JSON violan las reglas de integridad
    referencial o cuando un archivo individual tiene un error de estructura."""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# Helpers internos
# ─────────────────────────────────────────────────────────────────────────────

def _parse_json_file(path: Path) -> Any:
    """Lee y parsea un archivo JSON.  Si falla, lanza DataIntegrityError con la
    ruta exacta del archivo problemático para facilitar el diagnóstico."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        raise DataIntegrityError(
            f"Error de sintaxis JSON en '{path}': {exc}"
        ) from exc


def _load_json_file(filename: str) -> list[dict[str, Any]]:
    """Carga un archivo JSON simple (array) desde data/.  Solo se usa para
    recursos que aún NO se han migrado a estructura de directorios."""
    file_path = _DATA_ROOT / filename
    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de datos: {file_path}")
    return _parse_json_file(file_path)


# ─────────────────────────────────────────────────────────────────────────────
# Loaders principales (estructura de directorios)
# ─────────────────────────────────────────────────────────────────────────────

def load_classes() -> dict[str, ClassData]:
    """Carga las clases desde data/classes/*.json.
    Cada archivo contiene un único objeto JSON con los datos de una clase.
    El slug del archivo debe coincidir con el campo 'slug' dentro del JSON.
    """
    classes_dir = _DATA_ROOT / "classes"
    if not classes_dir.is_dir():
        raise FileNotFoundError(
            f"No se encontró el directorio de clases: '{classes_dir}'. "
            "Asegúrate de que exista 'data/classes/' con un .json por clase."
        )

    result: dict[str, ClassData] = {}
    for json_path in sorted(classes_dir.glob("*.json")):
        raw = _parse_json_file(json_path)
        try:
            obj = ClassData(**raw)
        except (TypeError, KeyError) as exc:
            raise DataIntegrityError(
                f"El archivo '{json_path}' no cumple el esquema ClassData: {exc}"
            ) from exc
        result[obj.slug] = obj

    return result


def load_subclasses() -> dict[str, SubclassData]:
    """Carga las subclases desde data/subclasses/<class_slug>/*.json.
    Usa rglob para encontrar todos los .json de forma recursiva.
    Cada archivo contiene un único objeto JSON con los datos de una subclase.
    """
    subclasses_dir = _DATA_ROOT / "subclasses"
    if not subclasses_dir.is_dir():
        raise FileNotFoundError(
            f"No se encontró el directorio de subclases: '{subclasses_dir}'. "
            "Asegúrate de que exista 'data/subclasses/<class>/' con un .json por subclase."
        )

    result: dict[str, SubclassData] = {}
    for json_path in sorted(subclasses_dir.rglob("*.json")):
        raw = _parse_json_file(json_path)
        try:
            obj = SubclassData(**raw)
        except (TypeError, KeyError) as exc:
            raise DataIntegrityError(
                f"El archivo '{json_path}' no cumple el esquema SubclassData: {exc}"
            ) from exc
        result[obj.slug] = obj

    return result


# ─────────────────────────────────────────────────────────────────────────────
# Loaders secundarios (archivo único por recurso)
# ─────────────────────────────────────────────────────────────────────────────

def load_species() -> dict[str, SpeciesData]:
    data = _load_json_file("species.json")
    return {item["slug"]: SpeciesData(**item) for item in data}


def load_backgrounds() -> dict[str, BackgroundData]:
    data = _load_json_file("backgrounds.json")
    return {item["slug"]: BackgroundData(**item) for item in data}


def load_feats() -> dict[str, FeatData]:
    data = _load_json_file("feats.json")
    return {item["slug"]: FeatData(**item) for item in data}


def load_spells() -> dict[str, SpellData]:
    data = _load_json_file("spells.json")
    return {item["slug"]: SpellData(**item) for item in data}


def load_weapons() -> dict[str, WeaponData]:
    data = _load_json_file("weapons.json")
    return {item["slug"]: WeaponData(**item) for item in data}


def load_armor() -> dict[str, ArmorData]:
    data = _load_json_file("armor.json")
    return {item["slug"]: ArmorData(**item) for item in data}


def load_equipment() -> dict[str, EquipmentData]:
    data = _load_json_file("equipment.json")
    return {item["slug"]: EquipmentData(**item) for item in data}


# ─────────────────────────────────────────────────────────────────────────────
# Validación de integridad referencial cruzada
# ─────────────────────────────────────────────────────────────────────────────

def validate_all(repo) -> None:
    """Valida referencias cruzadas entre todas las entidades cargadas.
    Lanza DataIntegrityError con un mensaje descriptivo ante cualquier
    inconsistencia."""
    valid_abilities = {"STR", "DEX", "CON", "INT", "WIS", "CHA"}

    # 1. Reglas de Clases
    for cls in repo.list_classes():
        # Validar nivel de subclase (Siempre 3 en 5.5e 2024)
        if cls.subclass_level != 3:
            raise DataIntegrityError(
                f"La clase {cls.slug} tiene subclass_level {cls.subclass_level}, debe ser 3."
            )

        # Validar requisitos de multiclaseo
        for req in cls.multiclass_requirements:
            if req.get("ability") not in valid_abilities:
                raise DataIntegrityError(
                    f"Clase {cls.slug}: Requisito de multiclaseo usa habilidad inválida "
                    f"'{req.get('ability')}'."
                )
            if "operator" in req and req["operator"] not in {"AND", "OR"}:
                raise DataIntegrityError(
                    f"Clase {cls.slug}: Operador de multiclaseo inválido '{req['operator']}'."
                )

        # Validar opciones de equipo (El slug especial "gp" representa monedas
        # de oro y se omite de la validación de referencia.)
        for choice_group in cls.equipment_choices:
            for item in choice_group:
                item_slug = item.get("slug")
                if item_slug == "gp":
                    continue
                if not (
                    repo.get_weapon(item_slug)
                    or repo.get_armor(item_slug)
                    or repo.get_equipment(item_slug)
                ):
                    raise DataIntegrityError(
                        f"Clase {cls.slug}: El equipo '{item_slug}' en "
                        f"equipment_choices no existe."
                    )

    # 2. Referencias de Subclases
    for sub in repo.list_subclasses():
        if not repo.get_class(sub.class_slug):
            raise DataIntegrityError(
                f"Subclase {sub.slug}: Referencia a la clase inexistente '{sub.class_slug}'."
            )

    # 3. Referencias de Trasfondos
    for bg in repo.list_backgrounds():
        if not repo.get_feat(bg.origin_feat_slug):
            raise DataIntegrityError(
                f"Trasfondo {bg.slug}: Referencia a la dote de origen inexistente "
                f"'{bg.origin_feat_slug}'."
            )

    # 4. Reglas de Dotes (Feats)
    for feat in repo.list_feats():
        for asi in feat.asi:
            if asi.get("ability") not in valid_abilities:
                raise DataIntegrityError(
                    f"Dote {feat.slug}: Otorga ASI a una habilidad inválida "
                    f"'{asi.get('ability')}'."
                )

    # 5. Referencias de Conjuros
    for spell in repo.list_spells():
        for class_slug in spell.classes:
            if not repo.get_class(class_slug):
                raise DataIntegrityError(
                    f"Conjuro {spell.slug}: Referencia a la clase inexistente '{class_slug}'."
                )
        for subclass_slug in spell.subclasses:
            if not repo.get_subclass(subclass_slug):
                raise DataIntegrityError(
                    f"Conjuro {spell.slug}: Referencia a la subclase inexistente "
                    f"'{subclass_slug}'."
                )