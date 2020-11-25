# MidiGenerator

## Overview

Collection of Recipes for Algorithmic Music Generation.
This folder builds on MusiStrata (https://github.com/Wally869/MusiStrata) to represent a musical structure and output midi files, to be further processed in a DAW or soundfont-based synthesizer, such as fluidsynth.

THIS IS A WIP. This Branch is experimental and a lot of things are likely to be broken. Please make an issue if you encounter an issue.  

## Dependencies

- MusiStrata (https://github.com/Wally869/MusiStrata)
- Mido (https://github.com/mido/mido)

## Generators  

### Rhythmic Generators  
- Rhythmic Model  
Generate a sequence of MusiStrata.SoundEvent elements by drawing Duration values to pack a preselected bar duration (number of beats per bar).  
- Rhythmic Preset  
Generate a sequence of SoundEvents by drawing subsequences from a pre-made preset and variants 

### Melodic Models
- Distance Picker Model  
From a given array of height-ordered allowed notes, and knowing the starting note, pick a new note at random. Notes weights are determined by in-array position distance from the previous note, and subjected to a decaying factor. This allows to replicate the stability property often found in melodies  
- From Interval Picker Model  
Pick a new note by considering a previous note, an array of potential target notes, and an array of allowed intervals. This can allow to create successions of consonances, or very flexible notes succession (for example, allowing in your model the use of a minor harmonic scale, which flattens the 7th note in the scale when descending from the 8th).  
- Scale Follower Picker Model  
Create a succession of notes from a scale. Basically a scale arpeggio.  











