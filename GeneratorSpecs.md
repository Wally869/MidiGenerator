# Generator Specifications

## Rhythmic Models

### Preset Definition
Create Probability Presets for rythmic patterns generation.
Presets must be defined in a json file in the "RhythmicModels" folder contain the following fields:
- Name: str  
For tracking purposes
- Tags: [str]  
For tracking purposes, as well as for definition of global song presets 
- SilenceChance: float
Probability of drawing a Silence
- Notes: Dict[str: float]  
Keys are duration for notes, values are the probability associated with drawing the given duration
- Silences: Dict[str: float]
Same as Notes, but for silences


### Example
```json
{
  "Name": "Test1",
  "Tags": ["Test"],
  "SilenceChance": 0.1,
  "Notes": {
    "0.5": 0.1,
    "1": 0.5,
    "1.5": 0.4
  },
  "Silences": {
    "0.5": 0.25,
    "1":  0.75
  }
}
```

### Remarks
Presets are loaded to generate RythmicModel objects. These objects parse the json files of the presets, and ensure that the sum of probabilities for the defined elements sums to 1.   
  
WARNING - When defining a Preset, you need to make sure to have your silences and notes go to the same level of detail so that bars can always sum up to an integer.

For example: if Notes in the example above had a duration of 0.25, Silences would have needed a possible duration of 0.25, else the RhythmicModel.GenerateBarPreset will end up in an infinite loop, since it might not find a solution (the generator loops until it finds a solution to generating a succession of notes and silences up to the specified number of beats).
