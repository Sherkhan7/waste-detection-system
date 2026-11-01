"""Waste class -> bin mapping and short facts. Edit to match your dataset's classes."""

BINS = {
    "paper":   {"name": "Blue bin",   "color": "#2f7de1", "accepts": "Paper & cardboard"},
    "plastic": {"name": "Yellow bin", "color": "#f5c518", "accepts": "Plastic & metal packaging"},
    "metal":   {"name": "Yellow bin", "color": "#f5c518", "accepts": "Plastic & metal packaging"},
    "glass":   {"name": "Green bin",  "color": "#2e9e5b", "accepts": "Glass bottles & jars"},
    "organic": {"name": "Brown bin",  "color": "#8b5a2b", "accepts": "Food & garden waste"},
    "general": {"name": "Gray bin",   "color": "#7a7f87", "accepts": "Non-recyclable waste"},
}

FACTS = {
    "paper":   "Recycling one tonne of paper saves about 17 trees' worth of fibre.",
    "plastic": "A plastic bottle can take around 450 years to break down.",
    "metal":   "Recycling aluminium uses about 95% less energy than making it new.",
    "glass":   "Glass can be recycled again and again without losing quality.",
    "organic": "Food waste in landfill produces methane, a strong greenhouse gas.",
    "general": "Before binning it, ask: can this be reused, repaired or avoided?",
}

# Maps raw model labels (e.g. TACO / COCO-style names) to the 6 classes above.
LABEL_ALIASES = {
    "bottle": "plastic", "plastic bottle": "plastic", "cup": "plastic", "bag": "plastic",
    "can": "metal", "tin": "metal", "carton": "paper", "cardboard": "paper",
    "newspaper": "paper", "wine glass": "glass", "jar": "glass",
    "banana": "organic", "apple": "organic", "orange": "organic", "food": "organic",
}


def resolve(label: str) -> dict:
    key = LABEL_ALIASES.get(label.lower(), label.lower())
    if key not in BINS:
        key = "general"
    return {"waste_class": key, "bin": BINS[key], "fact": FACTS[key]}
