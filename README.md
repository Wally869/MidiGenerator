# MidiGenerator

## Overview

Utils and classes to algorithmically generate Music.
This folder builds on MidiStructurer (https://github.com/Wally869/MidiStructurer) to represent a musical structure and  output a midi.

## Dependencies

- MidiStructurer (https://github.com/Wally869/MidiStructurer)
- Mido (https://github.com/mido/mido)

## A Layered Approach

To generate music, I decided on an incremental approach, which more or less follows the following steps:
- Decide on the composition of the song in terms of tracks (i.e. for example I want a solo track, a comping track and a percussions track)
- Generate rythms for the tracks. The algorithm generate "sections" to give structure to the track, but the rythms of these sections is dependent on the generation model selected
- Once the rythm has been set for the "melodic track" (i.e. the main track of our song, think singer or solo), a main scale, as well neighbouring scales are chosen and are set to the generated sections
- Notes are then picked from the given scales, according to a generator preset. 
- Finally accompanying/comping tracks also have rythms generated, and notes are set. The Bars of the main track are checked when generating these secondary tracks to ensure the notes picked sound alright

After that, the song is passed to the MidiStructurer converter and a midi file is generated.

## Generators

The main challenge of generating music is the sheer amount of possibilities:
you can play on the type of tracks used, their number, the instruments chosen, the scales, the rythmic preset etc...

I want to make it easy to extend the number of possibilities at generation, but this is still in development, more details will be given later. See [GeneratorSpecs.md](DevNotes/GeneratorSpecs.md) for more details

 





