# Anaslysis and visualization scripts for study one and two

```study_one.ipynb``` contains analsysis and visualization for study one

- calls ```scr/scr_analysis_functions_fyp``` for loading, preprocessing, and transforming scr data
- imports ```scr/behavioral_analysis_functions``` for loading and preprocessing (trait and state) self-report data

```study_two.ipynb``` contains analysis and visualization for study two data
    
- calls ```scr/adapting_fyp_analysis.py``` for loading, preprocessing, and transforming scr data
- imports ```gaze/gaze_analysis_objects.pkl```, gaze data that have already been preprocessed
- imports ```self_report/behavioral_analysis_objects.pkl```, self-report data (trait and state) that have - already been preprocessed

Figures and a brief description of results are in ```results_and_figures/```

```
TO DO:
- show that (trait and state) self-report measures dont predict renewal
-- 'expect_shock' in particular
-- setup for "What does?"
- find 'expect_shock' equivalent in day_two data
- is there any way that we can say that personal distress people overgeneralize? 
-- that is, they're learning something, but it's just too vague ...  
- finalize things today and 'release' a version on github that works perfectly
-- including data munging
-  include a mean analysis for each subject
-- can we predict each subject's baseline from anything?
- bring trait-level measures on study_one
``` 
