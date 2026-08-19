"""
Bonus B2: embodied-carbon reference data for >=5 representative materials.
Source: Inventory of Carbon and Energy (ICE) Database v3.0, Circular Ecology /
University of Bath (Jones & Hammond, 2019) - cradle-to-gate (A1-A3) figures,
generic/average values (not manufacturer-specific, since the BoQ names no brand).
Matched to materials by keyword against the `material` field in boq_items.py.
"""

CARBON_REFERENCE = [
    dict(match=("reinforcement", "tmt", "mild steel", "cold twisted", "t-iron", "guard flat",
                "fan clamp", "ms "),
         density=7850, gwp_per_kg=2.363,
         source="ICE Database v3.0 (Circular Ecology, Univ. of Bath, 2019) - steel, general/rebar"),
    dict(match=("cement concrete", "khurra", "gola", "plinth protection", "flooring 1:2:4"),
         density=2400, gwp_per_kg=0.130,
         source="ICE Database v3.0 (Circular Ecology, Univ. of Bath, 2019) - concrete, 30-35 MPa, general mix"),
    dict(match=("brick masonry", "half brick", "brick tiles"),
         density=1800, gwp_per_kg=0.240,
         source="ICE Database v3.0 (Circular Ecology, Univ. of Bath, 2019) - brick, common fired clay"),
    dict(match=("aluminium",),
         density=2700, gwp_per_kg=8.240,
         source="ICE Database v3.0 (Circular Ecology, Univ. of Bath, 2019) - aluminium, general (33% recycled)"),
    dict(match=("timber", "wood work", "wood door", "wood plug", "flush door"),
         density=600, gwp_per_kg=0.420,
         source="ICE Database v3.0 (Circular Ecology, Univ. of Bath, 2019) - timber, general hardwood sawn"),
    dict(match=("terrazzo", "marble"),
         density=2700, gwp_per_kg=0.079,
         source="ICE Database v3.0 (Circular Ecology, Univ. of Bath, 2019) - marble/dimension stone"),
    dict(match=("cement plaster", "cement mortar finish"),
         density=1900, gwp_per_kg=0.157,
         source="ICE Database v3.0 (Circular Ecology, Univ. of Bath, 2019) - mortar (1:6 cement:sand, general)"),
    dict(match=("bitumen", "bitumastic"),
         density=1050, gwp_per_kg=0.380,
         source="ICE Database v3.0 (Circular Ecology, Univ. of Bath, 2019) - bitumen"),
]


def lookup_carbon(material_label: str):
    label = (material_label or "").lower()
    for ref in CARBON_REFERENCE:
        if any(k in label for k in ref["match"]):
            return ref
    return None
