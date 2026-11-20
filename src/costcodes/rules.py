"""MasterFormat division names and the keyword rules used to pick one.

Division names follow the common 2004 numbering (two digit divisions).
The keyword lists are this project's own and cover the usual construction
and facility cost descriptions; they are not an official classification.
"""
from __future__ import annotations

DIVISIONS: dict[str, str] = {
    "01": "General Requirements",
    "02": "Existing Conditions",
    "03": "Concrete",
    "04": "Masonry",
    "05": "Metals",
    "06": "Wood, Plastics and Composites",
    "07": "Thermal and Moisture Protection",
    "08": "Openings",
    "09": "Finishes",
    "10": "Specialties",
    "11": "Equipment",
    "12": "Furnishings",
    "13": "Special Construction",
    "14": "Conveying Equipment",
    "21": "Fire Suppression",
    "22": "Plumbing",
    "23": "Heating, Ventilating and Air Conditioning",
    "26": "Electrical",
    "27": "Communications",
    "28": "Electronic Safety and Security",
    "31": "Earthwork",
    "32": "Exterior Improvements",
    "33": "Utilities",
}

KEYWORDS: dict[str, tuple[str, ...]] = {
    "01": ("mobilization", "permit fee", "general conditions", "supervision", "temporary",
           "dumpster", "project management", "insurance", "bond", "cleanup", "scaffold"),
    "02": ("demolition", "demo ", "abatement", "asbestos", "selective removal", "survey"),
    "03": ("concrete", "rebar", "slab", "footing", "formwork", "grout", "cement"),
    "04": ("masonry", "brick", "cmu", "block wall", "mortar", "stone veneer"),
    "05": ("steel", "metal deck", "joist", "handrail", "railing", "angle iron", "welding"),
    "06": ("lumber", "framing", "plywood", "millwork", "casework", "cabinet", "blocking"),
    "07": ("roof", "roofing", "insulation", "waterproofing", "flashing", "sealant",
           "caulk", "vapor barrier", "membrane"),
    "08": ("door", "window", "glazing", "storefront", "hardware set", "overhead door",
           "curtain wall", "skylight"),
    "09": ("drywall", "gypsum", "paint", "flooring", "carpet", "ceiling tile", "tile",
           "plaster", "epoxy floor", "vinyl"),
    "10": ("signage", "toilet partition", "locker", "fire extinguisher", "corner guard",
           "bathroom accessories"),
    "11": ("kitchen equipment", "lab equipment", "loading dock equipment", "appliance"),
    "12": ("furniture", "window blinds", "shades", "seating"),
    "13": ("clean room", "pre-engineered", "pool", "tank"),
    "14": ("elevator", "escalator", "lift", "dumbwaiter", "hoist"),
    "21": ("sprinkler", "fire pump", "standpipe", "fire suppression", "clean agent"),
    "22": ("plumbing", "pipe", "piping", "water heater", "toilet", "sink", "backflow",
           "drain", "faucet", "domestic water"),
    "23": ("hvac", "duct", "air handler", "ahu", "chiller", "boiler", "vav", "thermostat",
           "diffuser", "exhaust fan", "controls bms", "refrigerant"),
    "26": ("electrical", "conduit", "panel", "wiring", "breaker", "transformer", "lighting",
           "light fixture", "generator", "switchgear", "receptacle"),
    "27": ("data cable", "network cabling", "telecom", "fiber", "wifi", "structured cabling"),
    "28": ("fire alarm", "card reader", "access control", "cctv", "camera", "intrusion",
           "smoke detector"),
    "31": ("excavation", "grading", "backfill", "earthwork", "trenching", "fill dirt"),
    "32": ("asphalt", "paving", "sidewalk", "curb", "landscaping", "fence", "striping",
           "irrigation"),
    "33": ("storm drain", "sewer", "water main", "manhole", "utility trench", "gas main"),
}
