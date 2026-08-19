# AMP-GEN AI/ML Intern Take-Home: Material Passport Extraction

Extracts all 64 BoQ line items (74 rows once multi-quantity sub-items are expanded)
from `BoQ_CBRI_Principals_Residence.pdf`: a scanned, dot-matrix + handwritten Bill of
Quantities, and classifies them into `AMP_Passport_Template.xlsx`'s Material Passport
schema.

## Run it (< 5 min)

```bash
pip install -r requirements.txt
python src/build_passport.py
```

Outputs land in `output/`:

- `passport_filled.xlsx`: template with rows 1-6 preserved, 74 classified rows appended
- `passport.json`: same data as JSON, one object per row
- `building_meta.json`: page-1 project metadata (Bonus B3)
- `visualization.png`: material category distribution chart

## What's in `src/`

- `boq_items.py`: raw transcription of all 64 BoQ items (source of truth, hand-read
  from the scanned pages, see APPROACH.md for why)
- `carbon_data.py`: ICE Database v3 embodied-carbon reference table (Bonus B2)
- `build_passport.py`: pipeline: expand sub-items → normalize units → map to
  Volume/Area/Length/Weight/Count → compute embodied carbon → write all 4 outputs

## Tools / LLMs / OCR disclosure

The source PDF has no text layer (confirmed via `pypdf`). Classical OCR was not
available locally and is a poor fit for dot-matrix + handwritten text anyway, so pages
were rendered to PNG (PyMuPDF, 200 DPI) and transcribed via direct vision reading
(disclosed per the task's own rules). Full reasoning and every judgment call made on
ambiguous quantities/codes is in `APPROACH.md`.

## Honest time estimate

- ~1.5 hr: locating the email, downloading attachments, assessing OCR difficulty
- ~2.5 hr: transcribing all 64 items + sub-items from 13 rendered pages
- ~2 hr: classification scheme, unit normalization, embodied-carbon matching, pipeline code
- ~1 hr: outputs, visualization, docs, git history

~7 hours total.

## Bonuses attempted

- **B2** (embodied carbon): done, 40 distinct materials / 51 rows have Density and
  GWP/kg, sourced from ICE Database v3, cited in each row's Comment field. Of those,
  35 rows also get a computed Embodied Carbon A1-A3 total: volume/weight rows compute
  it directly, and area/length/count rows compute it from a thickness, cross-section,
  or per-unit rate stated in the BoQ's own description text (see `AREA_TO_MASS` /
  `LENGTH_TO_MASS` / `COUNT_TO_MASS` in `build_passport.py`). The remaining 16 rows
  (mostly count-based ironmongery items with no stated per-unit mass, plus a couple
  of rows with no thickness stated at all) are left without a total rather than
  guessed.
- **B3** (building metadata): done, `output/building_meta.json`.
- **B1** (live deployment): `docs/index.html` is a dependency-free static viewer
  (fetches `../output/passport.json`, renders the table + `visualization.png`). It
  reads those paths relative to `docs/`, so GitHub Pages must serve the repo **root**
  (Settings → Pages → Deploy from branch → `main` / `/(root)`, not `/docs`: the
  `/docs` option would only publish the `docs/` folder itself and break the relative
  fetch to `output/`). Once enabled it's live at
  `https://tejaslamba2006.github.io/amp-gen-material-passport/docs/`.
- **B4** (video walkthrough): not attempted.

## Validate

```bash
python src/validate_passport.py
```

Checks every row has all GREEN (required) columns filled and every GREY (out-of-scope)
column left blank, per the template's Instructions sheet.

## Known limitations

- Page 1's "Class Designation of soil" field is cut off in the physical scan (not a
  rendering issue) and recorded as `null`.
- A few DSR codes (item 28, item 62) could not be confidently attributed to their
  source row from the scan layout and are left blank.
