

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
