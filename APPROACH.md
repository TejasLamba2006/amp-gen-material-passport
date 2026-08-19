# Approach

## Tools used, and why

The source BoQ (`BoQ_CBRI_Principals_Residence.pdf`) has **no embedded text layer**:
confirmed with `pypdf`'s `extract_text()` returning empty strings on every page. It's a
scanned dot-matrix typewriter document with hand-written quantities filled in by pen.
No local OCR engine (tesseract) was installed, and classical OCR is a poor fit here
regardless: dot-matrix fonts and handwriting are exactly the cases where OCR engines
produce garbled, low-confidence output that still needs manual verification.

Instead I rendered each page to a PNG at 200 DPI with **PyMuPDF** (`fitz`) and read the
images directly as a vision task, transcribing all 64 BoQ line items (descriptions,
quantities, units, DSR 1989 codes) by eye. This is the disclosed method per the task's
own ground rules ("Any tools/LLMs/OCR allowed, but disclose in APPROACH.md"). One page-1
field ("Class Designation of [soil]") is physically cut off at the bottom edge of the
scan (confirmed with a 400 DPI crop of that region, not a rendering artifact), so it's
recorded as `null` in `building_meta.json` with a note.

Everything downstream (classification, unit normalization, xlsx/json/chart generation)
is a reproducible Python pipeline (`src/`), not manual spreadsheet editing:

- `src/boq_items.py`: raw transcription, one dict per BoQ Sl.No., with sub-items where
  the scan lists multiple quantities under one item (e.g. item 16 centring/shuttering
  has 5 sub-quantities, item 51 CI fittings has 3).
- `src/carbon_data.py`: embodied-carbon reference table (ICE Database v3, Circular
  Ecology / Univ. of Bath) matched by material keyword, for bonus B2.
- `src/build_passport.py`: expands sub-items, normalizes units, maps quantities to the
  correct Volume/Area/Length/Weight/Count column, computes embodied carbon where
  applicable, and writes `output/passport_filled.xlsx`, `output/passport.json`,
  `output/building_meta.json`, `output/visualization.png`.

Item count check: 64 top-level BoQ items + 10 extra sub-item rows (items 16, 17, 31, 32,
34, 51 each have 2-5 sub-quantities) = 74 total rows. The page-1 footer states
"No of Items: 64", which matches the top-level count. That's a useful sanity check that
no item was skipped or double-counted.

## Judgment calls (documented, not asked mid-task)

- **Item 4 quantity** ("5.4" vs "S.4"/"[.4"): read as 5.4. Unit printed as "100 Sq.m"
  (a DSR convention meaning the quantity is counted in hundreds of sqm), so the derived
  area is 540 sqm, captured in `Derived Quantity` / `Derived Quantity Basis`.
- **Item 15's "0.]"**: read as 0.1 cum, consistent with the small scale of the other
  RCC column quantities on the same page.
- **Item 17.ii (cold-twisted/TMT reinforcement)**: the scan shows "1375.0/1500.0*" with
  a footnote that the starred figure applies to Seismic Zone V. It's ambiguous which
  number carries the asterisk from the scan alone. I used **1375.0 kg** as the base
  quantity and noted the 1500.0 kg Zone-V alternate in the row's Comment field, since
  the building's seismic zone metadata (page 1) lists "Zone I to IV and V," meaning both
  apply depending on site, so the base figure is the safer default.
- **Items 19-23 (brick class) and 24-25 (wood species)**: the source BoQ leaves these
  blank with an explicit footnote, "appropriate class designation of bricks/wood
  species may be incorporated before calling tenders." This is a genuine blank in the
  original document, not a scan defect, so `Material / Product` records this honestly
  rather than guessing a class/species.
- **DSR code-to-item alignment on page 6 (items 26-29)**: DSR codes print at the top of
  each item's row block, vertically aligned with the first line of that item's
  description. For this run of short items the vertical alignment is tight enough that
  a couple of codes (item 28 in particular) could not be confidently attributed and are
  left blank rather than guessed. Flagged here for a reviewer with the source PDF in
  hand to confirm.
- **Excluded items**: pure earthwork/labour operations (excavation, backfill, surface
  dressing, anti-termite chemical treatment, formwork/centring-shuttering) are tagged
  `[EXCLUDED] <reason>` in Comment rather than assigned a fabricated embodied-carbon
  material, since they don't leave permanent building fabric (formwork is removed;
  excavated earth briefly redeployed) or the embodied mass is negligible relative to
  measurement precision (chemical treatment).
- **Embodied carbon (Bonus B2)**: matched by material keyword against the ICE Database
  v3 (Circular Ecology, Univ. of Bath, 2019), using generic/average figures since the BoQ
  specifies mix ratios (e.g. "1:2:4") and DSR generic materials rather than named
  manufacturers/brands. 40 distinct materials across 51 rows got density + GWP/kg
  values (well above the ≥5 minimum), covering concrete, steel, masonry, aluminium,
  timber, terrazzo/marble, plaster, and bitumen.
- **Embodied carbon totals for area/length/count rows**: volume and weight rows
  convert straight to mass. For area/length/count rows, many BoQ descriptions state
  an explicit thickness, cross-section, or per-unit rate (e.g. item 40 "40 mm thick"
  CC flooring, item 10 "1.7 Kg. per square metre" bitumen coat, item 43 glass strip
  "40 mm wide and 6 mm thick") were parsed into a small lookup
  (`AREA_TO_MASS`/`LENGTH_TO_MASS`/`COUNT_TO_MASS` in `build_passport.py`) and used to
  compute a real A1-A3 total for 19 additional rows (35/51 total, up from 16/51).
  Two entries needed a judgment call, flagged in-row via Comment: items 22/23
  (half-brick masonry) have no thickness stated on the scan, so the standard 115mm
  nominal is assumed; item 47 (gola) uses its full 15x15cm stated cross-section as an
  upper-bound approximation of the actual filleted profile. Items 42 and 55 are
  multi-layer assemblies (marble/terrazzo over a different-material underlayer), so
  mass uses only the top finish layer's stated thickness, and the Comment says so.
  The remaining 16 rows (count-based ironmongery with no stated per-unit mass, item 45's
  lime-concrete-plus-brick-tile composite, and a couple of rows with no thickness
  stated at all) are left without a total rather than guessed.

## What worked

- Vision-based transcription handled the dot-matrix + handwritten mix reliably; cross-
  checking the "No of Items: 64" footer against the actual transcribed count caught
  that nothing was skipped.
- A single data file (`boq_items.py`) + one build script kept the pipeline reproducible
  and let unit normalization / carbon lookup / column mapping be verified in one pass
  rather than 74 manual spreadsheet edits.

## What didn't work / limitations

- A handful of DSR codes (item 28, item 62) couldn't be confidently attributed from
  the scan's layout and are left blank rather than guessed.
- "Class Designation of soil" (page 1 metadata) is unrecoverable: physically cut off
  in the source scan, not just cropped in rendering.
- No live OCR confidence scores exist since this wasn't classical OCR. `Material
  Confidence` is set qualitatively (High for classified materials, Medium for
  excluded/ambiguous rows) rather than from a numeric OCR engine score.

## Next steps with 2 more weeks

1. Get the original PDF re-scanned or request the paper original to resolve the
   cut-off soil classification field and the 2-3 ambiguous DSR codes.
2. Replace the keyword-matched embodied-carbon lookup with per-item material-specific
   figures (e.g. distinguish PCC 1:5:10 vs RCC 1:2:4 densities/carbon rather than one
   "cement concrete" bucket) and add A4-A5 (transport + construction) stages if the
   brief expands beyond A1-A3.
3. Add automated tests around `normalize_unit()`/`quantity_column()` and a schema
   validator that checks every generated row against the template's GREEN/AMBER/GREY
   column expectations before export.
4. Pursue bonus B1 (live deployment): a small static viewer over `passport.json`.
