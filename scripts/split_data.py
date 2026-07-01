import json
from pathlib import Path

# 1. Split classes.json -> data/classes/<slug>.json
classes_dir = Path('data/classes')
classes_dir.mkdir(parents=True, exist_ok=True)

with open('data/classes.json', 'r', encoding='utf-8') as f:
    classes = json.load(f)

for cls in classes:
    slug = cls['slug']
    out_path = classes_dir / f'{slug}.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(cls, f, ensure_ascii=False, indent=2)
    print(f'Created: {out_path}')

# 2. Split subclasses.json -> data/subclasses/<class_slug>/<slug>.json
subclasses_dir = Path('data/subclasses')
subclasses_dir.mkdir(parents=True, exist_ok=True)

with open('data/subclasses.json', 'r', encoding='utf-8') as f:
    subclasses = json.load(f)

for sub in subclasses:
    slug = sub['slug']
    class_slug = sub['class_slug']
    class_dir = subclasses_dir / class_slug
    class_dir.mkdir(parents=True, exist_ok=True)
    out_path = class_dir / f'{slug}.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(sub, f, ensure_ascii=False, indent=2)
    print(f'Created: {out_path}')

print('\nDone! Summary:')
print(f'  Classes: {len(classes)} files in data/classes/')
print(f'  Subclasses: {len(subclasses)} files in data/subclasses/<class>/')
