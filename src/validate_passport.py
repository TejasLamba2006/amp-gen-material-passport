"""
Sanity-checks output/passport.json against the template's GREEN/GREY column rules.

GREEN columns must be filled for every row (Schedule Item Code is exempt --
a few DSR codes are genuinely blank in the source scan, see APPROACH.md).
GREY columns (circularity/detachability/lifespan) must stay blank -- they're
explicitly out of scope per the Instructions sheet.

Run: python src/validate_passport.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASSPORT_JSON = os.path.join(ROOT, "output", "passport.json")

GREEN_REQUIRED = [
    "GMAP Id", "BOQ Item No.", "Description", "Floor / Section", "Discipline",
    "Material / Product", "Material Category", "Original Quantity", "Original Unit",
    "Schedule (DSR/SOR)",
]
QUANTITY_COLUMNS = ["Volume (m³)", "Area (m²)", "Length (m)", "Weight (kg)", "Count (Nos)"]
GREY_MUST_BE_BLANK = [
    "% Reused", "% Available for Reuse", "Assumed Construction Waste", "Waste Codes",
    "Detachability – Connection", "Detachability – Connection Detail",
    "Detachability – Accessibility", "Detachability – Intersection",
    "Detachability – Product Edge", "Lifespan (Years)",
]


def validate(rows):
    errors = []
    for row in rows:
        rid = row.get("BOQ Item No.", "?")

        for col in GREEN_REQUIRED:
            if row.get(col) in (None, ""):
                errors.append(f"row {rid}: required GREEN column '{col}' is blank")

        if not any(row.get(c) is not None for c in QUANTITY_COLUMNS):
            errors.append(f"row {rid}: no quantity column (Volume/Area/Length/Weight/Count) is filled")

        for col in GREY_MUST_BE_BLANK:
            if row.get(col) not in (None, ""):
                errors.append(f"row {rid}: GREY column '{col}' should be blank but has {row.get(col)!r}")

    return errors


def main():
    with open(PASSPORT_JSON, encoding="utf-8") as f:
        rows = json.load(f)

    errors = validate(rows)
    print(f"Checked {len(rows)} rows.")
    if errors:
        print(f"{len(errors)} issue(s):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("All GREEN columns filled, all GREY columns blank. OK.")


if __name__ == "__main__":
    main()
