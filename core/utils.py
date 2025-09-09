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
    r"\b(dog|dogs|puppy|cat|cats|kitten|rabbit|rabbits|bunny|hamster|hamsters|guinea\s*pig|guinea\s*pigs|bird|birds|parrot|parrots)\b",
    re.I,
)

REFLECT = {
    "am": "are", "are": "am",
    "i": "you", "you": "I",
    "me": "you", "my": "your", "your": "my",
    "mine": "yours", "yours": "mine",
    "myself": "yourself", "yourself": "myself",
}   

def reflect(text: str) -> str:
    """Token-wise reflection that preserves capitalization and punctuation spacing."""
    import re
    tokens = re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)
    out = []
    for t in tokens:
        low = t.lower()
        if low in REFLECT:
            repl = REFLECT[low]
            if t and t[0].isupper():
                repl = repl[0].upper() + repl[1:]
            out.append(repl)
        else:
            out.append(t)
    # Re-join with spaces only between alphanumeric neighbors
    joined = []
    for i, tok in enumerate(out):
        if i > 0 and tok.isalnum() and joined[-1].isalnum():
            joined.append(" ")
        joined.append(tok)
    return "".join(joined)

def normalize_species(s: str | None):
    if not s: return None
    s = s.lower()
    if s in {"puppy"}: return "dog"
    if s in {"dog", "dogs"}: return "dog"
    if s in {"kitten"}: return "cat"
    if s in {"cat", "cats"}: return "cat"
    if s in {"bunny"}: return "rabbit"
    if s in {"rabbit", "rabbits"}: return "rabbit"
    if s in {"hamster", "hamsters"}: return "hamster"
    if "guinea" in s: return "guinea pig"
    if s in {"bird", "birds"}: return "bird"
    if s in {"parrot", "parrots"}: return "parrot"
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


