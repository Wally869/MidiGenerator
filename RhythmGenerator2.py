from enum import Enum
from typing import List, Dict
from typing_extensions import Self
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from random import choice


@dataclass_json
@dataclass
class RhythmElement:
    beat: float
    duration: float


class RhythmGenerator:
    def __init__(self) -> None:
        pass


class PresetPart(Enum):
    Main = 0
    Variant = 1


class RhythmPresetGenerator:
    def __init__(self, name: str, main_preset: List[RhythmElement], variants: List[List[RhythmElement]] = []) -> None:
        self.name = name
        self.main_preset: List[RhythmElement] = main_preset
        self.variants: List[List[RhythmElement]] = variants

    def __str__(self) -> str:
        return "<RhythmPresetGenerator - {}>".format(self.name)
    
    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        return RhythmPresetGenerator(
            data["name"],
            main_preset=[
                RhythmElement(
                    elem["beat"],
                    elem["duration"]
                ) for elem in data["main_preset"]
            ],
            variants=[
                [
                    RhythmElement(
                        elem["beat"],
                        elem["duration"]
                    ) for elem in variant
                ]
                for variant in data["variants"]
            ]
        )

    def gen_pattern(self, preset_parts: List[PresetPart], nb_bars: int) -> List[List[RhythmElement]]:
        """

        """
        default_to_main = len(self.variants) == 0

        curr_variant_id = 0
        curr_parts_id = 0
        output: List[List[RhythmElement]] = []
        while len(output) < nb_bars:
            if curr_variant_id >= len(self.variants):
                curr_variant_id = 0
            if curr_parts_id >= len(preset_parts):
                curr_parts_id = 0
            if preset_parts[curr_parts_id] == PresetPart.Main:
                output.append(self.main_preset)
            else:
                if default_to_main:
                    output.append(self.main_preset)
                else:
                    output.append(self.variants[curr_variant_id])
                    curr_variant_id += 1
            curr_parts_id += 1

        return output

    def gen_random_pattern(self, nb_bars: int) -> List[List[RhythmElement]]:
        all_parts = [self.main_preset] + self.variants
        return [choice(all_parts) for _ in range(nb_bars)]
