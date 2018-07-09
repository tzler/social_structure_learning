# Anaslysis and visualization scripts for study one and two

```results/study_one.ipynb``` contains analsysis and visualization for study one

- calls ```scr/scr_analysis_functions_fyp``` for loading, preprocessing, and transforming scr data
- imports ```scr/behavioral_analysis_functions``` for loading and preprocessing (trait and state) self-report data

```results/study_two.ipynb``` contains analysis and visualization for study two data
    
- calls ```scr/adapting_fyp_analysis.py``` for loading, preprocessing, and transforming scr data
- imports ```gaze/gaze_analysis_objects.pkl```, gaze data that have already been preprocessed
- imports ```self_report/behavioral_analysis_objects.pkl```, self-report data (trait and state) that have - already been preprocessed

Figures and a brief description of results in ```results/```

    TO DO:
    - find 'expect_shock' equivalent in day_two data
    - is there any way that we can say that personal distress people overgeneralize? 
        - that is, they're learning something, but it's just too vague ...  
    - finalize things today and 'release' a version on github that works perfectly
    -  include a mean analysis for each subject
        - can we predict each subject's baseline from anything?
    - bring trait-level measures on study_one
