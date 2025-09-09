from core.engine import build_engine, respond_with_context

def reply(text, ctx=None):
    eng = build_engine()
    ctx = ctx or {"species": None, "age_months": None, "weight_kg": None}
    r, _ = respond_with_context(eng, text, ctx)
    return r

def test_vaccines_cat():
    assert "FVRCP" in reply("What vaccines does a kitten need?")

def test_deworm():
    assert "deworm" in reply("How often should I deworm a puppy?").lower()

def test_fleas():
    assert "monthly flea/tick" in reply("Best treatment for fleas for dogs?").lower()

def test_spay():
    r = reply("When to spay a female cat?")
    assert "4-6 months" in r

def test_diet():
    r = reply("Feeding plan for a 3 month old kitten")
    assert "kitten" in r.lower()

def test_emergency():
    r = reply("My dog has labored breath and pale gums")
    assert "urgent veterinary care" in r

def test_fallback():
    r = reply("Thanks")
    assert "vaccines" in r.lower()
