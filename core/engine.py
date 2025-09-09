import re
from .rules import rules
from .utils import extract_species, parse_age_months, parse_weight_kg

class Engine:
    def __init__(self, ruleset):
        self.rules = ruleset

def build_engine():
    return Engine(rules())

def respond_with_context(engine: Engine, text: str, ctx: dict[str, object]):
    updates = {}
    sp = extract_species(text)
    if sp: updates["species"] = sp
    age = parse_age_months(text)
    if age is not None: updates["age_months"] = age
    wt = parse_weight_kg(text)
    if wt is not None: updates["weight_kg"] = wt

    ctx2 = {**ctx, **updates}

    for r in engine.rules:
        if r.get("context"):
            continue
        m = r["pattern"].match(text)
        if m:
            return r["handler"](ctx2, m), updates

    return None, updates
