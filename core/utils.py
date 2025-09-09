import re

NUM = r"(?P<num>\d+(?:\.\d+)?)"

AGE = re.compile(
    rf"(?P<age>{NUM})\s*(?P<unit>month|months|mo|m|year|years|yr|y|week|weeks|w)\b",
    re.I,
)

WEIGHT = re.compile(
    rf"(?P<w>{NUM})\s*(?P<wunit>kg|kilograms?|lb|lbs|pounds?)\b",
    re.I,
)

SPECIES = re.compile(
    r"\b(dog|puppy|cat|kitten|rabbit|bunny|hamster|guinea\s*pig|bird|parrot)\b",
    re.I,
)

def normalize_species(s: str | None):
    if not s: return None
    s = s.lower()
    if s in {"puppy"}: return "dog"
    if s in {"kitten"}: return "cat"
    if s in {"bunny"}: return "rabbit"
    if "guinea" in s: return "guinea pig"
    return s

def parse_age_months(text: str):
    m = AGE.search(text)
    if not m: return None
    n = float(m.group("age"))
    u = m.group("unit").lower()
    if u.startswith("y"):
        return int(round(n * 12))
    if u.startswith("w"):
        return int(round(n * 4.345))
    return int(round(n))

def parse_weight_kg(text: str):
    m = WEIGHT.search(text)
    if not m: return None
    n = float(m.group("w"))
    u = m.group("wunit").lower()
    if u in {"lb", "lbs", "pound", "pounds"}:
        return round(n * 0.453592, 2)
    return round(n, 2)

def extract_species(text: str):
    m = SPECIES.search(text)
    return normalize_species(m.group(1)) if m else None
