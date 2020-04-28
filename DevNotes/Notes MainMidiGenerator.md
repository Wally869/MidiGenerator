

### Flow

parameters fed to main generation function
what params:
- song structure
    - Tracks (melody, bass... and which instruments?)
    - patterning (AABA...)



from params, query DB for models descriptions
then create the rythm and melodic models


=> Think about main part of song first
everything is a variant on this

USE SECTIONS?
Yep
Create a Section class, that would have information on the scale used
implement a method to translate this section to another note?
Section would have tracks then

SO I have parts for a song
let's say this is a ABAB pattern, 2 parts alternating and repeating
how would I go about implementing this?

Well:
- What channels do they have?
- What instruments are used?
- What scale, what notes?
- Rhythm used in the parts

Couldn't I just consider this as a song within a song?
Would then have a 2 layered GenerateSong function (recursion is real nice when generating stuff)

have something like 
Song object, with Section attr
if len(Song.Sections) == 1:
    do the generation
else  
    [callMainFunction(Song(Sections=[s])) for section in Song.Sections]
    
but what about sections that should stay the same for the whole thing? like drums?
well exclude them i guess and recompose later

need structure object
make distinction:
- section
- section which is variant of other section
- constant track (like drums during whole song)

maybe compute all subsections in parallel? :monkaHmm:
reference them by name + id
maybe in object could say if has prototye

could give:
```json
{
  "section": "intro",
  "sectionId": 0,
  "trackType": "accompaniment",
  "trackTypeId": 1
}
```
allows to have several parts of a given type referenced (several bass for example)
also several part for a section (for example, drums at first, then bass come in in the intro section)

man this would be great:
the json/dict above would be the identifier of the section component
but section component COULD reference dependencies (for example: accompaniment might need melody component)

```python
class SectionComponent(object):
    def __init__(self):
        pass

```

so basically
but do I need the generators?

Section has:
- Name
- Scale
- Subsections (AB)
- TrackTypes (but that's for subsection?)

YOU KNOW WHAT BUD?
I CAN USE CLASSES!!!
AND query DB gives me potential input range for all this stuff
so then I can do choice poggers
=> I think this can be extended later?
Can set potential transformations compared to initial part?
for example chorus 2 can be a variation on chorus 1: basically same, but for example
different scale used, 


=> Get a specs object from db
=> fields are range?


now
for generation, maybe can use a target length
this allows for easy concatenation of same section (which would, in fact, be a sub section)
wait up
isn't that fucking smart?

sectionsNames = [
    "Intro", "Refrain", "Chorus", "Refrain", "Chorus", "Outro"
]
can be associated with 
sectionRepeat = [0, 1, 1, 1, 1, 0]
:monkaHmm:
still need subsections?