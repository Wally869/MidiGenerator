# How is development going?

### For presets management
use an in memory database?
buzhug looks pretty nice:
https://wiki.python.org/moin/buzhug
http://buzhug.sourceforge.net/

only for py2?
Use something else 
maybe tinydb
https://github.com/msiemens/tinydb
yeah sounds good

### 21/03/2020  
Created RythmicModels and RhythmicPresets generators.  
Rhythmic Models pick durations in a set of possibilities to create new patterns 
while RhytmicsPresets use predefined patterns.  

This distinction is necessary:
- Random patterns for melody
- Set Patterns for bass 

Need to implement note height selection for melody, and for other channels
Also need to implement instruments for percussions buddy ("percussion kit" when several, or possibility to use only one. Wil need tag to check true percussion or not)
Also, need for bass ostinato to have possibility of "root notes", i.e. note heights on which the other notes in the bar are based?
for example the bossa nova variations: 1 and 3 based beats, using 1 and 5 height.  
but can do variations: add beat at 2.5 which is a croche, and which is 1/2 or 1 tone below target note (at 5) 


### 23/03/2020
Created several note picking schemes, so should be good for melody generation  
Need to create some more for bass ostinato, or have a bass ostinato generator which is not a notepickermodel?

so yeah basically, need bass ostinato note setter, percussion kit instrument (note) setter depending on beats, and comping track generator and note setter


then it's off to generating presets and I'm done? 

for comping: what i can do is call it accompanying
can be like a choice, do i accompany the bass track, or the melodic track
then ok what degrees are playing? is it based on current scale, or follow current note

so ok, can choose: follow all notes of track, or only a few, or follow another rhythm

and ok which degrees? 3rd-5th-7th, alone or combination, above or below (chord inversions?)  

can also play on instruments: can play support for melody, with bass instrument
or play bass support with melody instrument, or even use 3rd instrument?

bass ostinato: 1 to 3 then 1 to 5 and alternate

### 25/03/2020

Implemented the drums track generation:
correctly mapping specs of instruments to a given track so is very nice

still to do:
- bass ostinato generator
- fix the accompanying stuff (get current scales and work on it? maybe use a scales succession preset?)

=> May be nice to add some operations on models for rhythms I guess, like "faster" or "slower" to adjust preset
=> also would be nice a scale change for bars: change notes depending on new scale? would be nice, plus I got all the stuff needed in scalesutils? (can vary between notes and heights) but not too useful for now I guess


### 26/03/2020

Fixed comping: gives out 3rd and 7th of scale so is ok
may need to introduce some variation on comping coz a bit flat? or maybe not needed
maybe probabilistic mode is nice enough

so now, maybe add ensuring nice smooth transition by selecting notes common to 2 scales?
ok this done

So finally, only bass ostinato remaining?



Will need to rewrite the generators somewhat

I'd like to introduce better structure in the composition of the melodic part (bars into segments, segments into track now, but would be nice to switcheroo between rhythmic models for segments?)

=> Could get structural inputs to create parts: for example for a 3 bars segment: 2 bars from fast model, 1 bar from slow model (see tour de france)

Can perform variation on only one bar of this thing then: the last one? 



Also, for comping could use some preset rhythm and give triads to play? maybe can also play on renversement de triads.

=> Connection, skip, leap? see counterpoint wikipedia



=> for comping/bass actually 

there is scale, but ALSO a succession of chords!!!! A chord is played at each beat (or intermittently) and is the same for the whole bar. Then next bar is changed chord, or same, at different scale, or same

this means, implement succession of scales and chords

IF len scales and len chords not the same, then by definition I will be looping differently?



![img](https://upload.wikimedia.org/wikipedia/commons/0/0a/Chord_progression.png)



that was from wiki

so actually, start from chords progression!

then ok that gives me my scales succession. This is given relative to C in this example, but I guess I can start from a different base scale	

=> here for chords succession https://www.fachords.com/jam-tracks-tool/, https://en.wikipedia.org/wiki/Chord_progression

chords succession don't necessarily loop. Whatev? (im thinking of bassline generation here, or more like, melodic base generation)