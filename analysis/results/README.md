# social\_structure\_learning

```description```

Social cues are thought to provide a teaching signal that enables learning about the environmental contingencies. In social fear conditioning, for example, it has been shown that observing a conspecific being shocked recruits many of the same neural mechanisms for conditioning to a direct US (e.g. the amygdala), and undergos the same well-characterized learning trajectories (e.g. conditioning and extinction). In these experiments, and much of the emotion literature, facial expressions are thought to act as an "unconditioned stimulus", much like a direct experience with an aversive event.  

```description```

### `study one`: psychological and physiological responses day one

Subjects differentially respond to a social "unconditioned stimulus" (US), operationalized as a demonstrator's expression of pain. 

<p align="center">
  <img style='width:40%' src="figures/study_one_first_us.png">
</p>

The self-reported pain (`post_selfPain`) that subjects experienced while watching the demonstrator throughout the experiment covaries with other phychological measures of interst: the amount of pain subjects thought the demonstrator felt (`post_otherPain`), the degree to which subject's felt like they could relate to the demonstrator (`post_relate`), as well as the degree to which subjects felt that they were similar to the demonstrator (`post_similar`).

<p align="center">
  <img style='width:80%' src="figures/study_one_post_selfPain.png">
</p>

There were also significant relationships between how aversive subjects rated a personal experience with an electrical shock (`pre_aversive`) with subjective reports of pain for both themselves (`post_selfPain`) and the demonstrator (`post_otherPain`) during conditioning. There was also a significant relationship between the voltage that subjects chose to administer to themselves (`pre_voltage`) with how much pain they reported experience while watching the demonstrator (`post_selfPain`); interestingly, this was an inverse relationship such that subjects who self-administered shock at a lower voltage reported feeling greater pain observing the demonstrator being shocked (`post_selfPain`). 

<p align="center">
  <img style='width:80%' src="figures/study_one_shock_relationships.png">
</p>


None of these self-report measures covary with any of the physiological measures on day one. 


<p align="center">
  <img style='width:80%' src="figures/study_one_self_report_non_physio.png">
</p>

### `study one`: psychological and physiological responses on day two

One day two, subjects were presented with the same stimuli used as CS+ on day one. First, we note a common effect of order of the magnitude of the skin conductance: regardless of the stimulus type, the magnitude of the SCR is greater for the stimulus presented first across all subjects: 

<p align="center">
  <img style='width:40%' src="figures/study_one_order_effects.png">
</p>

This is, however, an indiscriminate measure; it does not reflect differential learning that took place on day one. We can segment our analysis to look only at those subjects who showed differential learning on day one. In the analysese below, we refer to two measures of learning on day one. 

The first measure, which we refer to as **`contagion learning`**, makes explicit a common assumption in the emotional literature: that a social cue (e.g. facial experession) can act as an "unconditioned stimulus", much like a direct experience with a stressor (e.g. electrical shock), providing a teaching signal for learning about the environment through the experience of conspecifics. For social fear conditioning, for example, it has been shown that these stimuli recruit many of the same neural mechanisms necessary for conditioning to a direct US, and undergo the same well characterized learning trajectories. 

If this is indeed the mechanisms for social learning, subjects who show differential skin conductance responses to the US (occuring at six CS+ offsets) should be those subjects that have learned the CS-US pairing. 

Conversely, if social learning occurs via the same mechanisms in place for first person experience, we would expect that learning on day one would be best characterized by subjects' differential skin conductance response to the CS+ at on ***onset*** of CS presentation. For clarity, we refer to this measure of learning as **`predictive learning`**. 

We show, first, that contrary to a common assumption in the literature, our measure of **`contagion learning`** does not accout for any variance in the physiological data on day two. 

as well as those subjects who showed differential emotional contagion on day one, at different threshholds: 

<p align="center">
  <img style='width:100%' src="figures/segmentation_analyis_contagion_study_one.png">
</p>

We show, first, that subjects whose skin conductance evidenced predictive learning showed significantly renewal on day two. This is true across as range of thresholds
 
<p align="center">
  <img style='width:100%' src="figures/segmentation_analyis_prediction_study_one.png">
</p>

And, finally, we can show that there is a continuous relationship between predictive learning with renewal, but not emotional contagion:  

<p align="center">
  <img style='width:100%' src="figures/day_one_scr_comparision.png">
</p>

#### `study one`: relationship between self-report measures and renewal

Only those subjects who report believing that the demonstrator was actually being shocked, on day one, reported expecting that they would be shocked on day two. 

<p align="center">
  <img style='width:40%' src="figures/day_one_expectation_and_belief.png">
</p>

These behavioral measures, however, do not appear to predict renewal on day two. 

<p align="center">
  <img style='width:80%' src="figures/day_one_self_report_non_renewal.png">
</p>

Additionally, we can look at the full covariance matrix of self-report and phsysiological (`contagion`, `prediction`, and `renewal`) and see that there is not much off-diagonal structure relating behavioral and physiological measures: 

<p align="center">
  <img style='width:80%' src="figures/covariace_matrix_study_one.png">
</p>

This overall pattern of data suggests that subjects' self-reported experiences don't predict our physiological measures of interest. In particular, there are no self-report measures that predict renewal. Are there other trait and state measures that might predict renewal? 

## `study two`: replication 

First, we replicate the same pattern of physiological data we observed in study one. In this smaller cohort, there were no subjects who showed significantly differentially predictive responses to the CS+ on day one during conditioned, but looking across different statistical threshholds we observe the same pattern of evidence: predictive learning predicts renewal. 


<p align="center">
  <img style='width:100%' src="figures/segmentation_analyis_prediction_study_two.png">
</p>

Similarly, emotional contagion to the US on day one do not predict renewal: 


<p align="center">
  <img style='width:100%' src="figures/segmentation_analyis_contagion_study_two.png">
</p>


And again we observe a continuous relationship between these learning measures on day one with renewal:  

<p align="center">
  <img style='width:100%' src="figures/day_two_scr_comparision.png">
</p>

### `study two`: incorporting attentional measures

First, we observe that looking time at faces during shock covaries with self-report measures of interest: 

<p align="center">
  <img style='width:100%' src="figures/faces_and_self_report.png">
</p>

Yet this same measure does not predict our physiological measures of interest. 

<p align="center">
  <img style='width:100%' src="figures/faces_and_physio.png">
</p>

and neither do a number of self-report measures that should, ostensibly, scale with learning about other's pain: 

<p align="center">
  <img style='width:100%' src="figures/self_report_not_renewal.png">
</p>

There are, however, other measures that do predict renewal: the amount of pain subjects report feeling at experiencing the shock themselves (```self_pain```), trait-level personal distress (```personal_distress```) as measured by the IRI, and looking time at the model's wrist, at the time of the US (```US_onset_wrist```): 

<p align="center">
  <img style='width:100%' src="figures/self_report_renewal.png">
</p>


    TO DO
    - build a calssifier that incorporates ALL the data into a prediction of renewal
    - incorporate trait data into study one
