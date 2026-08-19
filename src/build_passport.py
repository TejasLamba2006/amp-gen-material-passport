"""
Builds output/passport_filled.xlsx, output/passport.json, output/building_meta.json
and output/visualization.png from src/boq_items.py.

Run: python src/build_passport.py
"""
import json
import os
import sys

from openpyxl import load_workbook

sys.path.insert(0, os.path.dirname(__file__))
from boq_items import ITEMS
from carbon_data import lookup_carbon

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "AMP_Passport_Template.xlsx")
OUT_DIR = os.path.join(ROOT, "output")

UNIT_MAP = {
    "cu.m": "cum", "cum": "cum", "m³": "cum",
    "sq.m": "sqm", "sqm": "sqm", "m²": "sqm",
    "mtr.": "m", "mtr": "m", "m": "m",
    "kg.": "kg", "kg": "kg",
    "each": "nos", "nos": "nos",
}


def normalize_unit(raw_unit: str):
    """Returns (normalized_unit, quantity_multiplier, derived_note)."""
    u = (raw_unit or "").strip().lower()
    if u == "100 sq.m":
        return "sqm", 100.0, "Unit printed as '100 Sq.m' (DSR per-100-sqm convention); quantity multiplied by 100"
    if u == "10 cubic decimetre":
        return "cum", 0.01, "Unit printed as '10 Cubic decimetre' = 0.01 cum per Instructions sheet"
    return UNIT_MAP.get(u, u), 1.0, ""


def quantity_column(unit: str):
    return {"cum": "volume", "sqm": "area", "m": "length", "kg": "weight", "nos": "count"}.get(unit)


def build_rows():
    """Expand ITEMS (with sub-items) into flat row dicts matching the 50-col schema."""
    rows = []
    gmap_seq = 1
    for item in ITEMS:
        entries = item["sub"] if item["sub"] else [dict(suffix="", label="", qty=item["qty"],
                                                          unit=item["unit"], code=item["code"])]
        for e in entries:
            boq_no = f"{item['no']}.{e['suffix']}" if e["suffix"] else item["no"]
            desc = item["desc"] if not e["label"] else f"{item['desc']} :: {e['suffix']}) {e['label']}"
            unit_norm, mult, unit_note = normalize_unit(e["unit"])
            qty_raw = e["qty"]
            qty_norm = round(qty_raw * mult, 4) if qty_raw is not None else None
            qcol = quantity_column(unit_norm) if qty_norm is not None else None

            comment_parts = []
            if item["excluded"]:
                comment_parts.append(f"[EXCLUDED] {item['excluded']}")
            if unit_note:
                comment_parts.append(unit_note)
            if item["no"] == "17" and e.get("suffix") == "ii":
                comment_parts.append("Scan shows alternate qty 1500.0 Kg marked * for Seismic Zone V; "
                                      "1375.0 Kg used as base figure (ambiguous which value the * applies to)")
            if item["no"] in ("19", "20", "21", "22", "23"):
                comment_parts.append("Brick class designation left blank in source BoQ per footnote "
                                      "('appropriate class designation of bricks may be incorporated "
                                      "before calling tenders') - not a scan defect")
            if item["no"] in ("24", "25"):
                comment_parts.append("Wood species left blank in source BoQ per the same footnote")
            if e.get("code") in ("N.S.I.",):
                comment_parts.append("N.S.I. = Non-Schedule Item (rate outside DSR 1989)")

            carbon = None if item["excluded"] else lookup_carbon(item["material"])
            if carbon:
                comment_parts.append(f"Embodied carbon source: {carbon['source']}")

            row = {
                "GMAP Id": f"GMAP-{gmap_seq:03d}",
                "BOQ Item No.": boq_no,
                "Article Number": "",
                "External DB Id": "",
                "Description": desc,
                "Floor / Section": item["section"],
                "Discipline": item["discipline"],
                "Material / Product": item["material"],
                "All Materials Detected": item["material"],
                "Material Category": item["category"],
                "Material Confidence": "Medium" if item["excluded"] else "High",
                "Grade": item["grade"],
                "Mix Ratio": item["grade"],
                "Original Quantity": qty_raw,
                "Original Unit": e["unit"],
                "Volume (m³)": qty_norm if qcol == "volume" else None,
                "Area (m²)": qty_norm if qcol == "area" else None,
                "Length (m)": qty_norm if qcol == "length" else None,
                "Weight (kg)": qty_norm if qcol == "weight" else None,
                "Count (Nos)": qty_norm if qcol == "count" else None,
                "Derived Quantity": qty_norm if unit_note else None,
                "Derived Quantity Unit": unit_norm if unit_note else "",
                "Derived Quantity Basis": unit_note,
                "Density (kg/m³)": carbon["density"] if carbon else None,
                "Embodied Carbon A1-A3 (kg CO₂e)": None,
                "GWP / kg (kg CO₂e/kg)": carbon["gwp_per_kg"] if carbon else None,
                "Schedule (DSR/SOR)": "DSR 1989",
                "Schedule Item Code": e.get("code", ""),
                "Standard / Code Reference": "",
                "Classification (Matched)": "",
                "% Reused": None, "% Available for Reuse": None, "Assumed Construction Waste": None,
                "Waste Codes": "", "Detachability – Connection": "", "Detachability – Connection Detail": "",
                "Detachability – Accessibility": "", "Detachability – Intersection": "",
                "Detachability – Product Edge": "", "Lifespan (Years)": None,
                "Length (mm)": None, "Width (mm)": None, "Height (mm)": None, "Thickness (mm)": None,
                "Depth (mm)": None, "Diameter (mm)": None,
                "Unit Rate": None, "Total Cost": None, "Currency": "INR",
                "Comment": "; ".join(comment_parts),
            }
            if carbon and qty_norm is not None and row["Weight (kg)"] is None:
                mass_kg = None
                if qcol == "volume":
                    mass_kg = qty_norm * carbon["density"]
                if mass_kg:
                    row["Embodied Carbon A1-A3 (kg CO₂e)"] = round(mass_kg * carbon["gwp_per_kg"], 1)
            elif carbon and row["Weight (kg)"]:
                row["Embodied Carbon A1-A3 (kg CO₂e)"] = round(row["Weight (kg)"] * carbon["gwp_per_kg"], 1)

            rows.append(row)
            gmap_seq += 1
    return rows


def write_xlsx(rows):
    wb = load_workbook(TEMPLATE)
    ws = wb["Material Passport"]
    headers = [ws.cell(3, c).value for c in range(1, 51)]
    for i, row in enumerate(rows):
        r = 7 + i
        for c, h in enumerate(headers, start=1):
            ws.cell(r, c, row.get(h))
    out_path = os.path.join(OUT_DIR, "passport_filled.xlsx")
    wb.save(out_path)
    return out_path


def write_json(rows):
    out_path = os.path.join(OUT_DIR, "passport.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    return out_path


def write_building_meta():
    meta = {
        "name_of_work": "Construction of Principal's Residence (General-Modified), CBRI Roorkee",
        "location": "Central Building Research Institute (CBRI), Roorkee, Uttarakhand, India",
        "schedule": "Schedule 'A'",
        "depth_of_foundation_m": 0.60,
        "plinth_height_m": 0.45,
        "plinth_area_sqm": 90.6,
        "no_of_boq_items": 64,
        "seismic_zone": "Zone I-IV (base design); Zone V alternate reinforcement noted for item 17.ii",
        "safe_bearing_capacity": "10 T/Sq.m and above",
        "class_designation_of_soil": None,
        "class_designation_of_soil_note": "Illegible - physically cut off at the bottom edge of the scanned "
                                           "page 1 (confirmed via 400 DPI crop render, not a rendering artifact)",
        "rate_schedule": "DSR 1989 (Delhi Schedule of Rates)",
        "source_document": "BoQ_CBRI_Principals_Residence.pdf",
    }
    out_path = os.path.join(OUT_DIR, "building_meta.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    return out_path


def write_visualization(rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from collections import Counter

    counts = Counter(r["Material Category"] for r in rows if not r["Comment"].startswith("[EXCLUDED]"))
    categories = sorted(counts, key=lambda k: -counts[k])
    values = [counts[k] for k in categories]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(categories, values, color="#2b7a78")
    ax.set_xlabel("Number of BoQ line items")
    ax.set_title("Material Category Distribution — CBRI Principal's Residence BoQ")
    ax.invert_yaxis()
    for i, v in enumerate(values):
        ax.text(v + 0.1, i, str(v), va="center")
    fig.tight_layout()
    out_path = os.path.join(OUT_DIR, "visualization.png")
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = build_rows()
    xlsx_path = write_xlsx(rows)
    json_path = write_json(rows)
    meta_path = write_building_meta()
    viz_path = write_visualization(rows)
    print(f"Rows built: {len(rows)}")
    print(f"Wrote: {xlsx_path}")
    print(f"Wrote: {json_path}")
    print(f"Wrote: {meta_path}")
    print(f"Wrote: {viz_path}")


if __name__ == "__main__":
    main()
