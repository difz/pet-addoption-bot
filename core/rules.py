import re

def _disclaimer():
    return "\n\n_This is general guidance; consult a veterinarian for diagnosis/treatment._"

def rules():
    R = []

    # Context placeholder (conceptual; engine handles extraction)
    R.append({
        "name": "context_setter",
        "pattern": re.compile(r".*"),
        "handler": lambda ctx, m: None,
        "context": True
    })

    R.append({
        "name": "vaccines",
        "pattern": re.compile(r".*\b(vaccine|vaccination|shot|immuni[sz]ation|booster)s?\b.*", re.I),
        "handler": lambda ctx, m: _vaccines(ctx) + _disclaimer()
    })

    R.append({
        "name": "deworm",
        "pattern": re.compile(r".*\b(deworm|worm|worms|parasite|roundworm|tapeworm)\b.*", re.I),
        "handler": lambda ctx, m: _deworm(ctx) + _disclaimer()
    })

    R.append({
        "name": "fleas_ticks",
        "pattern": re.compile(r".*\b(flea|fleas|tick|ticks|mite|mites)\b.*", re.I),
        "handler": lambda ctx, m: _fleas(ctx) + _disclaimer()
    })


    R.append({
        "name": "spay_neuter",
        "pattern": re.compile(r".*\b(spay|neuter|sterili[sz]e|castrat(e|ion))\b.*", re.I),
        "handler": lambda ctx, m: _spay(ctx) + _disclaimer()
    })

    R.append({
        "name": "diet",
        "pattern": re.compile(r".*\b(feed\w*|diet\w*|food\w*|kibble|wet\s*food|raw)\b.*", re.I),
        "handler": lambda ctx, m: _diet(ctx) + _disclaimer()
    })


    R.append({
        "name": "pre_adopt_check",
        "pattern": re.compile(r".*\b(quarantine|isolate|vet\s*check|health\s*check|before\s*adopt|pre[- ]?adopt)\b.*", re.I),
        "handler": lambda ctx, m: _pre_check(ctx) + _disclaimer()
    })

    R.append({
        "name": "introductions",
        "pattern": re.compile(r".*\b(introduc|intro|meet|sociali[sz]e|aggress|fight)\b.*", re.I),
        "handler": lambda ctx, m: _introductions(ctx) + _disclaimer()
    })

    R.append({
        "name": "home_prep_cost",
        "pattern": re.compile(r".*\b(home|house|prep|setup|cost|budget|expense|suppl(y|ies))\b.*", re.I),
        "handler": lambda ctx, m: _home_cost(ctx) + _disclaimer()
    })

    R.append({
        "name": "emergency",
        "pattern": re.compile(
            r".*\b(vomit|diarrhea|bloody|not eat|won.?t eat|lethargy|seizure|collapse|labored\s*breath|trouble\s*breathing|pale gums)\b.*",
            re.I
        ),
        "handler": lambda ctx, m: _emergency(ctx) + _disclaimer()
    })

    R.append({
        "name": "fallback",
        "pattern": re.compile(r".*", re.I),
        "handler": lambda ctx, m: _fallback(ctx)
    })

    return R

# -------- handlers --------

def _species_age_line(ctx):
    s = ctx.get("species") or "pet"
    a = ctx.get("age_months")
    if a is None:
        return f"For your {s}"
    if a < 12:
        return f"For your {a}-month-old {s}"
    yrs = round(a/12, 1)
    return f"For your {yrs} year old {s}"

def _vaccines(ctx):
    sline = _species_age_line(ctx)
    s = ctx.get("species")
    if s in {"dog"}:
        return (f"{sline}: core vaccines include **DA2PP** (distemper/adenovirus/parvo/parainfluenza) "
                "and **rabies**. Typical puppy series: every 3-4 weeks until ~16 weeks, booster at 1 year, "
                "then every 1-3 years per vet and local law.")
    if s in {"cat"}:
        return (f"{sline}: core vaccines include **FVRCP** (panleukopenia/herpes/calicivirus) "
                "and **rabies**. Kitten series: every 3-4 weeks until ~16 weeks, booster at 1 year, "
                "then every 1-3 years per vet and local law.")
    return (f"{sline}: check local guidelines; most species need rabies (where applicable) "
            "plus species-specific cores. A vet will tailor the schedule.")

def _deworm(ctx):
    sline = _species_age_line(ctx)
    return (f"{sline}: routine deworming: young animals every 2 weeks until ~12 weeks, "
            "then monthly until 6 months, then every 3-6 months (or fecal checks). "
            "Use vet-approved products and dose by weight.")

def _fleas(ctx):
    sline = _species_age_line(ctx)
    return (f"{sline}: use a monthly flea/tick preventive suited to age/weight. "
            "Comb and inspect (neck, tail base, armpits). Treat the environment and wash bedding if infested.")

def _spay(ctx):
    s = ctx.get("species")
    sline = _species_age_line(ctx)
    if s == "dog":
        return (f"{sline}: typical spay/neuter timing is **6-9 months** (earlier for small breeds, "
                "later for some large breeds). Discuss growth/behavior with your vet.")
    if s == "cat":
        return (f"{sline}: typical spay/neuter timing is **4-6 months**; helps prevent roaming, spraying, and litters.")
    return f"{sline}: timing varies by species; consult your vet for safest anesthesia/age window."

def _diet(ctx):
    s = ctx.get("species")
    a = ctx.get("age_months")
    sline = _species_age_line(ctx)
    if s == "dog":
        base = "Puppies: 3 meals/day; adults: 2/day. Choose AAFCO-complete food."
        if a and a < 12: base += " Use **puppy** formula until ~12 months."
        return f"{sline}: {base} Start with label guide, adjust to keep a visible waist and palpable ribs."
    if s == "cat":
        base = "Kittens: 3–4 small meals/day; adults: 2–3/day. Choose AAFCO-complete food."
        if a and a < 12: base += " Use **kitten** formula until ~12 months."
        return f"{sline}: {base} Wet food can help hydration; avoid all-fish diets."
    return f"{sline}: follow species-appropriate, complete diets; avoid sudden switches. Provide fresh water always."

def _pre_check(ctx):
    sline = _species_age_line(ctx)
    return (f"{sline}: before adoption, schedule a vet exam within 48–72h, fecal test, "
            "deworming if needed, start core vaccines, microchip check, and external parasite check. "
            "Quarantine 7–10 days away from resident pets if history is unknown.")

def _introductions(ctx):
    sline = _species_age_line(ctx)
    return (f"{sline}: use **slow introductions**—scent swap first, then short supervised visuals, "
            "then brief meetings. Reward calm behavior. Separate resources (food bowls/litter boxes/bed).")

def _home_cost(ctx):
    s = ctx.get("species") or "pet"
    return (f"Home prep for your {s}: essentials include carrier/crate, bed, bowls, appropriate food, "
            "ID tag/microchip, parasite preventive, litter & box (cats) or potty plan (dogs), toys & enrichment. "
            "Budget: adoption fee + first vet visit/vaccines + preventive meds + supplies. "
            "Plan a recurring monthly cost for food and preventives.")

def _emergency(ctx):
    return ("**Red flags**: repeated vomiting/diarrhea, blood, not eating >24h (cats >12–18h), "
            "lethargy/weakness, breathing difficulty, seizures, pale/blue gums, trauma, poisoning. "
            "**Seek urgent veterinary care.**")

def _fallback(ctx):
    s = ctx.get("species")
    tip = "Tell me your planned pet (e.g., `I want to adopt a 3 month old kitten`) so I can tailor advice."
    return ("I can help with vaccines, deworming, fleas/ticks, diet, spay/neuter, "
            "quarantine & vet checks, introductions, home prep, costs, and emergencies.\n"
            + ("" if s else tip))
