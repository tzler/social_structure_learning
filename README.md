# social_structure_learning


Import environmental dependencies (e.g. python2.7, psychopy, pyserial) using anaconda with

    $ conda env create -f environment.yml

In 'analysis' are data and scripts (in progress) to test for renewal. In 'collection' are 
scripts for data collection. Hardware supported for data collection are
	
	- Eyetracker: Eyelink 1000
		
		Display managed by psychopy via 'EyelinkCoreGraphicsPsychopy' 
		a pylink script developed by Zhiguo Wang (zhiguo@sr-research.com)
		and 'tracker_functions' in this repository.  
 
	- Skin Conductance: BIOPAC MP150

		Triggers for experimental onset and stimulus events handled by
		pyserial, with the conversion from USB to parallel port via 
		Black Box (http://www.blackboxtoolkit.com/usbttl.html)

	- Electrical stimulation: SD9 STIMULATOR

		Triggered by pyserial via an arduino board 
		(https://store.arduino.cc/arduino-uno-rev3) 

Given this hardware, the experiment can be run in data_collection/ with

    $ python experiment_main.py

This script imports three modules, 'instructions', 'stimuli', and 'exit_questions'
that perform each section of data collection. In addition to loading packages 
for stimulis presentation (psychopy), communicating with hardware (os) or 
command line operations (os), these scripts also call helper functions coordinate
the hardware with the experiment. For each segment, these functions are

  instructions:

    - keyboard_input: Contains functions for collecting numeric and alphabetic
      key presses, and handling user input to the hardware

    - experiment_ports: Contains functions for finding, selecting, and then
      communicating with hardware--in this case, the SD9 for administering
      shock

  stimuli:

      - experiment_ports: In this case, opens the biopac and signals relevant
        stimulus markers across the experiment

      - tracker_functions: main interface for coordinating the eyelink hardware
        for collecting gaze data, as well as toggling the experimental display
        between the eyelink and experimental hard drives. configures monitor,
        signals eyelink with relevant stimuli, aligns frames for later analysis,
        performs drift correction across experiment, saves data, etc. etc. etc.

      - design_parameters: Loads design parameters like stimulus length, design
        structure, and the indices for marking events

  exit_questions:

      - keyboard_inputs: Collects subjects responses to questions from slides in
        instruction_slides/, aggregates these responses with those from
        'instructions' and saves self report data.

If you have any questions, contact me at tyler.ray.bonnen@gmail.com :) 
