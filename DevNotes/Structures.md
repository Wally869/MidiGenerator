### STRUCTURES

Descriptions
- Strophic
    - Constant repetition of a section (AAAAA)
- Medley
    - Infinite succession of self-contained sections (ABCDE...), sometimes with repetition (AABBCCDDEE...)
- Binary
    - Alternating between 2 sections (ABAB). Repetition possible (AABB). Can have variation (AA'BB')
- Ternary
    - 2 parts arranged in trio fashion (ABA)
- Rondo
    - Recurring section alternating with other sections, which will repeat (ABACADACABA), this is symmetrical rondo
    - Can also be assymetrical (ABACADAEA)
    - There is another form, arch form, with no main theme repetition (ABCBA)



### structs definition

song:
- has intro?
- inner structure
- has outro?

    
### How to proceed

2 levels of structure: 
- the song structure, divided in parts
- the part itself

SO:  
Define a music genre, which will restrict to possibilities of structures  
For example, can have intro or not? Outro or not? Do i add breaks?

Example: atmospheric track. To me seems more likely to be of Strophic structure than Through-Composed or Medley.
Binary for atmospheric track seems ok too.


So, at init time, I get to define the different components of the song  
But these components, I can also 


### Describing a song

```python
class Song(object):
    channels = ["Melody", "Bass", "Support", "Drums"]
    sequences = [seq0, seq1, seq0]
```

so i need a sequence object? or call it segment i guess
```python
class Segment(object):
    channels=["Melody", "Bass"]

```

Not gonna work coz I'm not taking scale into account?



# Thinking

let's take example  
song that does AAAA (strophic form)  
i got melody, bass, percussions?
how would I do this?

Well, generate the whole segment, which would then be repeated
All tracks are more or less independent



### NOTES

for variations inspiration:
32 Variations on an Original Theme in C minor, Beethoven

