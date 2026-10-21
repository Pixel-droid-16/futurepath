"""Shared read-only catalogue. Update JSON in data/; not code in the API."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/'data'
def load(name):
    return json.loads((DATA/name).read_text(encoding='utf8'))
SKILLS=load('skills.json')
SKILL_INDEX={s['id']:s for s in SKILLS}
ROLES=load('roles.json')
RESOURCES=load('learning_resources.json')
