"""
Raw transcription of BoQ_CBRI_Principals_Residence.pdf (Schedule 'A', items 1-64),
read directly from the scanned dot-matrix pages via LLM vision (see APPROACH.md).

Each entry is one BoQ Sl.No. `sub` holds sub-clauses (i, ii, iii...) that share the
parent description but have their own quantity/unit/code, matching how the scan lists
things like item 16 (centring & shuttering, 5 sub-quantities) or item 51 (CI fittings).

Fields:
  no          BoQ Sl.No. (str)
  desc        item-of-work text (trimmed, not re-worded)
  section     Sub-Head / schedule grouping as printed on the scan
  qty, unit   quantity/unit as handwritten (unit exactly as printed)
  code        DSR 1989 Code No. (col 7); "" if not legibly attributable to this item
  material    short material/product label (judgment call)
  category    Material Category bucket (judgment call)
  discipline  Discipline bucket (judgment call)
  grade       mix ratio / grade string if stated, else ""
  excluded    reason string if this item has no real embodied material (labour/earthwork/etc), else ""
  sub         list of {suffix, qty, unit, code} for multi-quantity items, else []
"""

ITEMS = [
    dict(no="1", section="Sub-Head - I, Earth Work", discipline="Civil & Sitework",
         desc="Earth work in excavation in foundation trenches or drains not exceeding 1.5 m in width or "
              "10 Sq.m on plan including dressing of sides and ramming of bottoms, lift upto 1.5 m including "
              "getting out the excavated soil and disposal of surplus excavated soil as directed within a "
              "lead of 50 m in all types of soil except rocks.",
         qty=32.0, unit="Cu.m", code="2.8", material="Earthwork (excavation)", category="Earthwork",
         grade="", excluded="earth + labour; negligible embodied material carbon"),

    dict(no="2", section="Sub-Head - I, Earth Work", discipline="Civil & Sitework",
         desc="Filling available excavated earth (excluding rock) in trenches, plinth, sides of foundations "
              "etc. in layers not exceeding 20 cm in depth consolidating each deposited layer by ramming "
              "& watering, lead upto 50 m and lift upto 1.5 m.",
         qty=12.0, unit="Cu.m", code="2.26", material="Earthwork (filling)", category="Earthwork",
         grade="", excluded="reused excavated earth + labour; no new material"),

    dict(no="3", section="Sub-Head - I, Earth Work", discipline="Civil & Sitework",
         desc="Filling the plinth with fine sand under floors including watering, ramming consolidating and "
              "dressing complete.",
         qty=11.0, unit="Cu.m", code="2.28", material="Fine sand (plinth fill)", category="Earthwork",
         grade=""),

    dict(no="4", section="Sub-Head - I, Earth Work", discipline="Civil & Sitework",
         desc="Surface dressing of the ground including removing vegetation, and inequalities not exceeding "
              "15 cm deep and disposal of rubbish, lead upto 50 m and lift upto 1.5 m in soft/loose soil.",
         qty=5.4, unit="100 Sq.m", code="2.29.1", material="Earthwork (surface dressing)", category="Earthwork",
         grade="", excluded="labour only; no material"),

    dict(no="5", section="Sub-Head - I, Earth Work", discipline="Civil & Sitework",
         desc="Providing and injecting chemical emulsion for PRECONSTRUCTIONAL anti termite treatment and "
              "creating a chemical barrier under and alround the column pits, wall trenches, basement "
              "excavation, top surface of plinth filling junction of wall and floor, along the external "
              "perimetre of building, expansion joints, surroundings of pipes & conduits etc. complete "
              "(plinth area of the building at ground floor only shall be measured) with Aldrin Emulsifiable "
              "Concentrate (0.5%)",
         qty=90.6, unit="Sq.m", code="2.35.2", material="Anti-termite chemical treatment", category="Chemical Treatment",
         grade="", excluded="chemical barrier application; negligible embodied material mass"),

    dict(no="6", section="Sub-Head - II, Concrete Work", discipline="Structural",
         desc="Providing and laying cement concrete in footings and bases for columns, excluding the cost "
              "of centring and shuttering with 1:5:10 (1 cement : 5 coarse sand : 10 graded stone aggregate "
              "40 mm nominal size).",
         qty=8.0, unit="Cu.m", code="4.5.10", material="Cement concrete 1:5:10", category="Concrete", grade="1:5:10"),

    dict(no="7", section="Sub-Head - II, Concrete Work", discipline="Structural",
         desc="Providing and laying cement concrete in retaining walls, return walls, walls (any thickness) "
              "including attached pilasters, buttresses, plinth, string courses, fillets etc. upto floor two "
              "level, excluding the cost of centring and shuttering with 1:5:10 (1 cement : 5 fine sand : 10 "
              "graded stone aggregate 40 mm nominal size)",
         qty=7.3, unit="Cu.m", code="4.6.11", material="Cement concrete 1:5:10", category="Concrete", grade="1:5:10"),

    dict(no="8", section="Sub-Head - II, Concrete Work", discipline="Structural",
         desc="Providing and laying upto floor two level cement concrete in string or lacing courses, "
              "parapets, copings, bed blocks anchor blocks, plain window sills and the like excluding "
              "centring and shuttering, etc. with 1:2:4 (1 cement : 2 coarse sand : 4 graded stone aggregate "
              "20 mm nominal size).",
         qty=0.1, unit="Cu.m", code="4.11.1", material="Cement concrete 1:2:4", category="Concrete", grade="1:2:4"),

    dict(no="9", section="Sub-Head - II, Concrete Work", discipline="Structural",
         desc="Providing and laying damp-proof course 40 mm thick with cement concrete 1:2:4 (1 cement : 2 "
              "coarse sand : 4 graded stone aggregate 12.5 mm nominal size)",
         qty=14.4, unit="Sq.m", code="4.24", material="DPC cement concrete 1:2:4", category="Concrete", grade="1:2:4"),

    dict(no="10", section="Sub-Head - II, Concrete Work", discipline="Structural",
         desc="Applying a coat of residual petroleum bitumen of penetration 80/100 of approved quality using "
              "1.7 Kg. per square metre on damp proof course after cleaning the surface with brushes and "
              "finally with a piece of cloth lightly soaked in kerosene oil.",
         qty=14.4, unit="Sq.m", code="4.27", material="Petroleum bitumen coating (DPC)", category="Waterproofing", grade=""),

    dict(no="11", section="Sub-Head - II, Concrete Work", discipline="Structural",
         desc="Reinforced cement concrete work in suspended floors, roofs, landings and balconies upto floor "
              "two level excluding cost of centring, shuttering, finishing and reinforcement with 1:2:4 (1 "
              "cement : 2 coarse sand : 4 graded stone aggregate 20 mm nominal size)",
         qty=11.3, unit="Cu.m", code="5.3", material="Reinforced cement concrete 1:2:4", category="Concrete", grade="1:2:4"),

    dict(no="12", section="Sub-Head - II, Concrete Work", discipline="Structural",
         desc="Reinforced cement concrete work in shelves upto floor two level excluding the cost of "
              "centering and shuttering and reinforcement with 1:2:4 (1 cement : 2 coarse sand : 4 graded "
              "stone aggregate 20 mm nominal size).",
         qty=1.0, unit="Cu.m", code="5.4", material="Reinforced cement concrete 1:2:4", category="Concrete", grade="1:2:4"),

    dict(no="13", section="Sub-Head - II, Concrete Work", discipline="Structural",
         desc="Reinforced cement concrete work in chajjas facias and gutters upto floor two level including "
              "throating of plastered drip and moulding excluding cost of centring, shuttering, finishing "
              "and reinforcement with 1:2:4 (1 cement : 2 coarse sand : 4 graded stone aggregate 20 mm "
              "nominal size).",
         qty=0.6, unit="Cu.m", code="5.5", material="Reinforced cement concrete 1:2:4", category="Concrete", grade="1:2:4"),

    dict(no="14", section="Sub-Head - II, Concrete Work", discipline="Structural",
         desc="Reinforced cement concrete work in lintels, beams, plinth beams and bresummers upto floor two "
              "level excluding the cost of centring, shuttering, finishing and reinforcement with 1:2:4 (1 "
              "cement : 2 coarse sand : 4 graded stone aggregate 20 mm nominal size).",
         qty=1.7, unit="Cu.m", code="5.6.3", material="Reinforced cement concrete 1:2:4", category="Concrete", grade="1:2:4"),

    dict(no="15", section="Sub-Head - II, Concrete Work", discipline="Structural",
         desc="Reinforced cement concrete work in columns, pillars, piers, abutments, posts and struts upto "
              "floor two level excluding the cost of centring, shuttering, finishing and reinforcement with "
              "1:2:4 (1 cement : 2 coarse sand : 4 graded stone aggregate 20 mm nominal size).",
         qty=0.1, unit="Cu.m", code="5.7.3", material="Reinforced cement concrete 1:2:4", category="Concrete", grade="1:2:4"),

    dict(no="16", section="Sub-Head - II, Concrete Work", discipline="Structural",
         desc="Centring and shuttering including strutting, proping etc. and removal of form work for :",
         qty=None, unit="", code="5.14", material="Formwork (temporary)", category="Formwork", grade="",
         excluded="temporary formwork, removed after casting; not part of final building fabric",
         sub=[
             dict(suffix="i", label="Suspended floors, roofs, landings, balconies and chajjas", qty=108.0, unit="Sq.m", code="5.14"),
             dict(suffix="ii", label="Shelves", qty=17.0, unit="Sq.m", code="5.14"),
             dict(suffix="iii", label="Lintels, beams, plinth beams, girders, bressumers and cantilever", qty=19.0, unit="Sq.m", code="5.14"),
             dict(suffix="iv", label="Columns, pillars, posts and struts", qty=2.0, unit="Sq.m", code="5.14"),
             dict(suffix="v", label="Vertical and horizontal fins individually or forming box louvers hand and facias", qty=9.0, unit="Sq.m", code="5.14"),
         ]),

    dict(no="17", section="Sub-Head - II, Concrete Work", discipline="Structural",
         desc="Reinforcement for RCC work including bending binding and placing in position complete.",
         qty=None, unit="", code="5.29", material="Reinforcement steel", category="Reinforcement", grade="",
         sub=[
             dict(suffix="i", label="Mild steel and medium tensile steel bars", qty=100.0, unit="Kg.", code="5.29"),
             dict(suffix="ii", label="Cold twisted bars (TMT); scan shows 1375.0 Kg, with 1500.0 Kg marked * "
                                     "applicable for Seismic Zone V (building is in Zone I-IV & V per page-1 metadata)",
                  qty=1375.0, unit="Kg.", code="5.29"),
         ]),

    dict(no="18", section="Sub-Head - II, Concrete Work", discipline="Structural",
         desc="Providing and laying upto floor two level RCC in string courses, bands, copings, bed plates, "
              "anchor blocks, plain window sills and the like excluding the cost of centering, shuttering, "
              "finishing and reinforcement with 1:2:4 (1 cement : 2 coarse sand : 4 graded stone aggregate "
              "20 mm nominal size).",
         qty=0.8, unit="Cu.m", code="5.16", material="Reinforced cement concrete 1:2:4", category="Concrete", grade="1:2:4"),

    dict(no="19", section="Sub-Head - III, Brick Work", discipline="Structural",
         desc="Brick work with bricks of class designation ____ in foundation and plinth in cement mortar "
              "1:6 (1 cement : 6 coarse sand).",
         qty=17.0, unit="Cu.m", code="6.1.14/6.5.1/6.5.2", material="Brick masonry (class designation left blank on scan)",
         category="Masonry", grade="CM 1:6"),

    dict(no="20", section="Sub-Head - III, Brick Work", discipline="Structural",
         desc="Brick work with bricks of class designation ____ in super structure above plinth upto floor "
              "two level in cement mortar 1:6 (1 cement : 6 coarse sand).",
         qty=40.3, unit="Cu.m", code="6.1.14/6.3/6.5.1/6.5.2", material="Brick masonry (class designation left blank on scan)",
         category="Masonry", grade="CM 1:6"),

    dict(no="21", section="Sub-Head - III, Brick Work", discipline="Structural",
         desc="Brick work 7 cm thick with bricks of class designation ------ in super structure upto floor "
              "two level in cement mortar 1:3 (1 cement : 3 coarse sand).",
         qty=0.9, unit="Sq.m", code="6.13/6.21/6.5.1/6.5.2", material="Brick masonry 7cm (class designation left blank on scan)",
         category="Masonry", grade="CM 1:3"),

    dict(no="22", section="Sub-Head - III, Brick Work", discipline="Structural",
         desc="Half brick masonry with bricks of class designation ____ in foundation & plinth in cement "
              "mortar 1:4 (1 cement : 4 coarse sand)",
         qty=4.8, unit="Sq.m", code="6.18.4/6.21/6.5.1/6.5.2", material="Half brick masonry (class designation left blank on scan)",
         category="Masonry", grade="CM 1:4"),

    dict(no="23", section="Sub-Head - III, Brick Work", discipline="Structural",
         desc="Half brick masonry with bricks of class designation ____ in super structure upto floor two "
              "level in cement mortar 1:4 (1 cement : 4 coarse sand).",
         qty=18.0, unit="Sq.m", code="6.18.4/6.19.1/6.20/6.21.1/6.21.2", material="Half brick masonry (class designation left blank on scan)",
         category="Masonry", grade="CM 1:4"),

    dict(no="24", section="Sub-Head - IV, Wood Work", discipline="Finishes",
         desc="Providing ____ wood work in frames of doors, windows, clerestory windows and other frames, "
              "wrought framed and fixed in position. (wood species left blank on scan; note 32 says species "
              "to be specified before tender)",
         qty=3.5, unit="10 Cubic decimetre", code="", material="Timber door/window frames", category="Timber", grade=""),

    dict(no="25", section="Sub-Head - IV, Wood Work", discipline="Finishes",
         desc="Providing and fixing 35 mm thick battended and framed door shutters of ____ wood including "
              "bright finished or/and black enamelled MS butt hinges with necessary screws.",
         qty=18.0, unit="Sq.m", code="", material="Timber door shutters (35mm battened)", category="Timber", grade=""),

    dict(no="26", section="Sub-Head - IV, Wood Work", discipline="Finishes",
         desc="Providing and fixing 25 mm thick flush door (for cupboard) shutters core of block board "
              "construction with frame of Ist class hard wood and well matched Ist class teak ply veneering "
              "with vertical grains or cross bands and face veneer on other face of shutters, including "
              "nickel plated bright finished MS piano hinges with necessary screws.",
         qty=4.7, unit="Sq.m", code="9.26.4", material="Flush door (block board, teak veneer)", category="Timber", grade=""),

    dict(no="27", section="Sub-Head - IV, Wood Work", discipline="Finishes",
         desc="Providing 50x50x50 mm 2nd class Teak wood plugs including cutting brick work and fixing in "
              "cement mortar 1:3 (1 cement : 3 fine sand) and making good the walls etc.",
         qty=20, unit="each", code="9.51", material="Teak wood plugs", category="Timber", grade=""),

    dict(no="28", section="Sub-Head - IV, Wood Work", discipline="Finishes",
         desc="Providing and fixing M.S. oxidised fan light vantilator catch with necessary screws etc. "
              "complete.",
         qty=6, unit="each", code="", material="MS oxidised ventilator catch", category="Ironmongery", grade=""),

    dict(no="29", section="Sub-Head - IV, Wood Work", discipline="Finishes",
         desc="Providing and fixing 90 mm oxidised M.S. hasp and staple (safety type) with necessaary "
              "screws etc. complete.",
         qty=2, unit="each", code="9.127.3", material="MS oxidised hasp and staple", category="Ironmongery", grade=""),

    dict(no="30", section="Sub-Head - V, Aluminium Work", discipline="Finishes",
         desc="Providing and fixing aluminium sliding door bolts 300 x 16 mm anodised transparent or dyed "
              "to required colour or shade with nuts and screws etc. complete.",
         qty=10, unit="Each", code="9.218.1", material="Aluminium sliding door bolts", category="Ironmongery", grade=""),

    dict(no="31", section="Sub-Head - V, Aluminium Work", discipline="Finishes",
         desc="Providing and fixing aluminium tower bolts anodised transparent or dyed to required colour "
              "or shade with necessary screws etc. complete.",
         qty=None, unit="", code="", material="Aluminium tower bolts", category="Ironmongery", grade="",
         sub=[
             dict(suffix="i", label="200 x 10 mm", qty=10, unit="Each", code="9.219.3"),
             dict(suffix="ii", label="100 x 10 mm", qty=8, unit="Each", code="9.219.5"),
         ]),

    dict(no="32", section="Sub-Head - V, Aluminium Work", discipline="Finishes",
         desc="Providing and fixing aluminium handles anodised transparent or dyed to required colour or "
              "shade with necessary screws etc. complete.",
         qty=None, unit="", code="", material="Aluminium handles", category="Ironmongery", grade="",
         sub=[
             dict(suffix="i", label="100 mm", qty=20, unit="Each", code="9.222.2"),
             dict(suffix="ii", label="75 mm", qty=4, unit="Each", code="9.222.3"),
         ]),

    dict(no="33", section="Sub-Head - V, Aluminium Work", discipline="Finishes",
         desc="Providing and fixing aluminium hanging floor door stopper anodised transparent or dyed to "
              "required colour & shade with necessary screws etc. complete.",
         qty=10, unit="Each", code="9.223", material="Aluminium floor door stopper", category="Ironmongery", grade=""),

    dict(no="34", section="Sub-Head - VI, Steel Work", discipline="MEP & Metal Work",
         desc="Providing and fixing steel glazed doors, windows and ventilators of standard rolled steel "
              "sections, joints mitred and welded with 15x3 mm lugs, 10 cm long, with steel lugs, embedded "
              "in cement concrete blocks 15x10x10 cm of 1:3:6 (1 cement : 3 coarse sand : 6 graded stone "
              "aggregate 20 mm nominal size) or with wooden plugs and screws or rawl plugs and screws or "
              "with fixing clips or with bolts and nuts as required, including providing and fixing of (Pin "
              "Head) 3mm thick glass panes with glazing clips and special metal sash putty of approved make "
              "complete including applying a priming coat of approved steel primer; excluding the cost of "
              "metal beading and other fitting except necessary hinges or pivots as required.",
         qty=None, unit="", code="N.S.I.", material="Steel glazed doors/windows/ventilators", category="Steel", grade="",
         sub=[
             dict(suffix="i", label="Windows - side hung", qty=11.3, unit="Sq.m", code="N.S.I."),
             dict(suffix="ii", label="Ventilators - centre hung", qty=1.0, unit="Sq.m", code="N.S.I."),
         ]),

    dict(no="35", section="Sub-Head - VI, Steel Work", discipline="MEP & Metal Work",
         desc="Providing and fixing oxidised mild steel casement window fastners of minimum weight 200 "
              "grams to side hung steel windows with necessary welding and machine screws etc. complete.",
         qty=21, unit="Each", code="N.S.I.", material="MS casement window fastners", category="Ironmongery", grade=""),

    dict(no="36", section="Sub-Head - VI, Steel Work", discipline="MEP & Metal Work",
         desc="Providing and fixing aluminium casement stays anodised transparent or dyed to requird colour "
              "and shade with with necessary welding and machine screws etc. complete.",
         qty=21, unit="Each", code="9.224", material="Aluminium casement stays", category="Ironmongery", grade=""),

    dict(no="37", section="Sub-Head - VI, Steel Work", discipline="MEP & Metal Work",
         desc="Providing and welding 20X4 mm M S Guard Flats 10cm c/c in steel windows of standard rolled "
              "steel section including a coat of steel primer as per drawing and specification complete in "
              "all respect.",
         qty=66.0, unit="Kg.", code="N.S.I.", material="MS guard flats", category="Steel", grade=""),

    dict(no="38", section="Sub-Head - VI, Steel Work", discipline="MEP & Metal Work",
         desc="Providing and fixing T - Iron frames for doors, windows and ventilators of mild steel Tee - "
              "sections, joints mitred and welded with 15x3 mm lugs 10 cm long embedded in cement concrete "
              "blocks 15x10x10 cm of 1:3:6 (1 cement : 3 coarse sand : 6 graded stone aggregate 20 mm "
              "nominal size) or with wooden plugs and screws or rawl plugs and screws or with fixing clips "
              "or with bolts and nuts as required, including fixing of necessary butt hinges and screws and "
              "applying a priming coat of approved steel primer.",
         qty=187.0, unit="Kg.", code="10.14", material="MS T-iron frames", category="Steel", grade=""),

    dict(no="39", section="Sub-Head - VI, Steel Work", discipline="MEP & Metal Work",
         desc="Providing and fixing MS fan clamp type I of 16 mm dia MS bar bent to shape with hooked ends "
              "in RCC slabs during laying including painting the exposed portion of loop, all as per "
              "standard design complete.",
         qty=5, unit="Each", code="10.19", material="MS fan clamp", category="Steel", grade=""),

    dict(no="40", section="Sub-Head - VII, Flooring", discipline="Finishes",
         desc="40 mm thick cement concrete flooring 1:2:4 (1 cement : 2 coarse sand : 4 graded stone "
              "aggregate 20.0 mm nominal size) finished with a floating coat of neat cement including "
              "cement slurry, rounding off edges and strips etc. but excluding the cost of nosing of steps "
              "etc. complete.",
         qty=68, unit="Sq.m", code="11.4.2", material="Cement concrete flooring 1:2:4", category="Concrete", grade="1:2:4"),

    dict(no="41", section="Sub-Head - VII, Flooring", discipline="Finishes",
         desc="18 mm thick cement plaster skirting (upto 30 cm height) with cement mortar 1:3 (1 cement : 3 "
              "coarse sand) finished with a floating coat of neat cement including rounding of junctions "
              "with floors.",
         qty=11.0, unit="Sq.m", code="11.10.1", material="Cement plaster skirting", category="Finishes/Plaster", grade="CM 1:3"),

    dict(no="42", section="Sub-Head - VII, Flooring", discipline="Finishes",
         desc="40 mm thick marble chips flooring, rubbed and polished to granolithic finish, under layer 31 "
              "mm thick cement concrete 1:2:4 (1 cement : 2 coarse sand : 4 graded stone aggregate 12.5 mm "
              "nominal size) and top layer 9 mm thick with white black, chocolate, grey yellow or Baroda "
              "green marble chips of sizes from 4 mm to 7 mm nominal size laid in cement marble powder mix "
              "3:1 (3 cement : 1 marble powder) by weight in proportion of 4:7 (4 cement marble powder mix "
              ": 7 marble chips) by volume including cement slurry etc., complete using dark shade pigment "
              "with ordinary cement.",
         qty=9.0, unit="Sq.m", code="11.16.1", material="Marble chip terrazzo flooring", category="Finishes/Flooring", grade="3:1 / 4:7"),

    dict(no="43", section="Sub-Head - VII, Flooring", discipline="Finishes",
         desc="Add or deduct for providing and fixing glass strips in joints of terrazo/cement concrete "
              "floors- 40 mm wide and 6 mm thick.",
         qty=18.0, unit="Mtr.", code="11.20.2", material="Glass strips (terrazzo joints)", category="Finishes/Flooring", grade=""),

    dict(no="44", section="Sub-Head - VIII, Roofing", discipline="Finishes",
         desc="Painting top of roofs with bitumen of approved quality at 17 Kg. per 10 square metre "
              "impregnated with a coat of coarse sand at 60 dm3 per 10 m2 including cleaning the slab "
              "surface with brushes and finally with a piece of cloth lightly soaked in kerosene oil "
              "complete with residual type petroleum bitumen of penetration 80/100.",
         qty=65.0, unit="Sq.m", code="12.29.1", material="Bitumen roof coating", category="Waterproofing", grade=""),

    dict(no="45", section="Sub-Head - VIII, Roofing", discipline="Finishes",
         desc="Lime concrete terracing on roofs, average thickness 10 cm laid to fall with 25 mm nominal "
              "size brick aggregate and 50% lime mortar 1:2 (1 lime putty : 2 surkhi) rammed and finished "
              "with gur and belgiri treatment complete and covered with flat FPS brick tiles of class "
              "designation 100 grouted with cement mortar 1:3 (1 cement : 3 fine sand) mixed with 5% crude "
              "oil by wt. of cement, over 12 mm layer of cement mortar 1:3 (1 cement : 3 fine sand) and "
              "finished neat.",
         qty=65.0, unit="Sq.m", code="12.35.2", material="Lime concrete terracing + FPS brick tiles", category="Waterproofing", grade="1:2"),

    dict(no="46", section="Sub-Head - VIII, Roofing", discipline="Finishes",
         desc="Providing and laying 25 mm thick burnt clay tiles 250x250x25 mm of approved quality over "
              "roofs with 1 cm side joints grouted with CM 1:3 (1 cement : 3 fine sand) over 15 mm thick bed "
              "of cement mortar 1:3 (1 cement : 3 fine sand) and finished neat.",
         qty=32.0, unit="Sq.m", code="N.S.I.", material="Burnt clay roof tiles 250x250x25mm", category="Finishes/Roofing", grade=""),

    dict(no="47", section="Sub-Head - VIII, Roofing", discipline="Finishes",
         desc="Providing gola 15x15 cm in size in cement concrete mix 1:3:6 (1 cement : 3 coarse sand : 6 "
              "graded stone aggregate 20 mm nominal size) covered with brick tiles in CM 1:3 (1 cement : 3 "
              "coarse sand) as per drawing and specifications complete in all respects.",
         qty=46.0, unit="Mtr.", code="N.S.I.", material="Gola (CC + brick tile edging)", category="Concrete", grade="1:3:6"),

    dict(no="48", section="Sub-Head - VIII, Roofing", discipline="MEP & Metal Work",
         desc="Making khurras 45 x 45 cm with average minimum thickness of 5 cm cement concrete 1:2:4 (1 "
              "cement : 2 coarse sand : 4 graded stone aggregate 20 mm nominal size) over PVC sheet 1m x 1m "
              "x 400 micron, finished with 12 cement plaster 1:3 (1 cement : 3 coarse sand) and a coat of "
              "neat cement rounding the edges and making and finishing the outlet complete.",
         qty=3, unit="Each", code="12.39", material="Khurra (roof drain outlet)", category="Waterproofing", grade=""),

    dict(no="49", section="Sub-Head - IX, Plumbing", discipline="MEP & Metal Work",
         desc="Providing and fixing on wallface 100 mm diameter CI rain water pipe including filling the "
              "joints with spun yarn soaked in neat cement slurry and cement mortar 1:2 (1 cement : 2 fine "
              "sand)",
         qty=10.0, unit="Mtr.", code="12.69.2", material="CI rain water pipe 100mm", category="Cast Iron Pipework", grade=""),

    dict(no="50", section="Sub-Head - IX, Plumbing", discipline="MEP & Metal Work",
         desc="Providing and fixing 100 mm dia MS holderbat clamps of approved design to CI or SCI rain "
              "water pipes embedded in and including cement concrete blocks 10 x 10 x 10 cm of 1:2:4 (1 "
              "cement : 2 coarse sand : 4 graded stone aggregate 20 mm nominal size) and cost of cutting "
              "holes and making good the walls etc.",
         qty=9, unit="Each", code="12.71.2", material="MS holderbat clamp", category="Ironmongery", grade=""),

    dict(no="51", section="Sub-Head - IX, Plumbing", discipline="MEP & Metal Work",
         desc="Providing and fixing on wall face CI accessories for rain water pipes including filling the "
              "joints with spun yarn soaked in neat cement slurry and cement mortar 1:2 (1 cement : 2 fine "
              "sand)",
         qty=None, unit="", code="", material="CI rain water pipe accessories", category="Cast Iron Pipework", grade="",
         sub=[
             dict(suffix="i", label="CI plain head 100 mm dia", qty=3, unit="Each", code="12.72.2.2"),
             dict(suffix="ii", label="CI plain shoe - 100 mm dia", qty=3, unit="Each", code="12.72.3.2"),
             dict(suffix="iii", label="CI plain bend - 100 mm dia", qty=3, unit="Each", code="12.72.1.2"),
         ]),

    dict(no="52", section="Sub-Head - X, Finishing", discipline="Finishes",
         desc="12 mm cement plaster of mix 1:6 (1 cement : 6 fine sand)",
         qty=220.0, unit="Sq.m", code="13.8.4", material="Cement plaster 12mm", category="Finishes/Plaster", grade="CM 1:6"),

    dict(no="53", section="Sub-Head - X, Finishing", discipline="Finishes",
         desc="15 mm cement plaster on the rough side of single or half brick wall of mix 1:6 (1 cement : 6 "
              "fine sand)",
         qty=220.0, unit="Sq.m", code="13.9.4", material="Cement plaster 15mm", category="Finishes/Plaster", grade="CM 1:6"),

    dict(no="54", section="Sub-Head - X, Finishing", discipline="Finishes",
         desc="6 mm cement plaster of mix 1:3 (1 cement : 3 fine sand) finished with a floating coat of "
              "neat cement and thick coat of lime wash on top of walls when dry for bearing of RCC slabs "
              "and beams.",
         qty=19.0, unit="Sq.m", code="13.25", material="Cement plaster 6mm", category="Finishes/Plaster", grade="CM 1:3"),

    dict(no="55", section="Sub-Head - X, Finishing", discipline="Finishes",
         desc="18 mm plastering with terrazzo finish for dado rubbed and polished complete, under layer 12 "
              "mm thick cement plaster 1:3 (1 cement : 3 coarse sand) and top layer 6 mm thick white, "
              "black, chocolate, grey, yellow or Baroda green marble chips of 3 mm and down size laid in "
              "cement marble powder mix 3:1 (3 cement : 1 marble powder) by weight in proportion of 4:7 (4 "
              "cement marble powder mix : 7 marble chips) by volume.",
         qty=20.0, unit="Sq.m", code="5.31/13.24.1", material="Terrazzo dado plaster", category="Finishes/Plaster", grade="3:1 / 4:7"),

    dict(no="56", section="Sub-Head - X, Finishing", discipline="Finishes",
         desc="Finishing and plastering the exposed surface of RCC with cement mortar 1:3",
         qty=155.0, unit="Sq.m", code="13.70.1", material="Cement mortar finish on exposed RCC", category="Finishes/Plaster", grade="CM 1:3"),

    dict(no="57", section="Sub-Head - X, Finishing", discipline="Finishes",
         desc="White washing with lime to give an even shade on new work (three or more coats).",
         qty=285.0, unit="Sq.m", code="13.73.1", material="Lime white wash", category="Finishes/Paint", grade=""),

    dict(no="58", section="Sub-Head - X, Finishing", discipline="Finishes",
         desc="Colour washing such as green, blue or buff to give an even shade on new work (two or more "
              "coats) with a base coat of white washing with lime.",
         qty=285.0, unit="Sq.m", code="13.81.1", material="Colour wash", category="Finishes/Paint", grade=""),

    dict(no="59", section="Sub-Head - X, Finishing", discipline="Finishes",
         desc="Applying priming coat with ready mixed pink or gray primer of approved brand and manufacture "
              "on wood work (hard and soft wood)",
         qty=47.0, unit="Sq.m", code="13.81.4", material="Wood primer coat", category="Finishes/Paint", grade=""),

    dict(no="60", section="Sub-Head - X, Finishing", discipline="Finishes",
         desc="Applying priming coat with readymixed zinc chromate yellow primer of approved brand and "
              "manufacture on steelwork (second coat)",
         qty=30.0, unit="Sq.m", code="13.84.3", material="Steel primer coat (zinc chromate)", category="Finishes/Paint", grade=""),

    dict(no="61", section="Sub-Head - X, Finishing", discipline="MEP & Metal Work",
         desc="Painting (two or more coats) on rain water, soil, waste and vent pipes and fittings with "
              "black anticorrosive bitumastic paint of approved brand and manufacture over and including a "
              "priming coat of ready mixed zinc chromate yellow primer on new work on 100 mm diameter "
              "pipes.",
         qty=10.0, unit="Mtr.", code="13.94.1", material="Bitumastic paint on CI pipework", category="Finishes/Paint", grade=""),

    dict(no="62", section="Sub-Head - X, Finishing", discipline="Finishes",
         desc="Painting with synthetic enamel paint of approved brand and manufacture to give an even shade "
              "in two or more coats on new work in black or chocolate shade over an under coat of suitable "
              "shade with ordinary paint of approved brand and manufacture.",
         qty=77.0, unit="Sq.m", code="", material="Synthetic enamel paint", category="Finishes/Paint", grade=""),

    dict(no="63", section="Sub-Head - X, Finishing", discipline="Finishes",
         desc="French spirit polishing two or more coats on new works including a coat of wood filler.",
         qty=13.0, unit="Sq.m", code="13.101.1", material="French spirit polish (wood)", category="Finishes/Paint", grade=""),

    dict(no="64", section="Sub-Head - X, Finishing", discipline="Civil & Sitework",
         desc="Making plinth protection 50 mm thick of cement concrete 1:3:6 (1 cement : 3 coarse sand : 6 "
              "graded stone aggregate 20 mm nominal size) over 75 mm bed of dry brick ballast 40 mm nominal "
              "size well rammed and consolidated and grouted with fine sand, including finishing the top "
              "smooth.",
         qty=34.6, unit="Sq.m", code="16.1", material="Plinth protection CC 1:3:6 over brick ballast", category="Concrete", grade="1:3:6"),
]

for _it in ITEMS:
    _it.setdefault("sub", [])
    _it.setdefault("excluded", "")
