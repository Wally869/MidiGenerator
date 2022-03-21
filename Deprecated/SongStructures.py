from __future__ import annotations


STRUCTURAL_TYPES = [
    "Sectional",
    "Developmental",
    "Variational"
]

SECTIONAL_FORMS = [
    "Strophic",
    "Medley", # or chain. Same as through composed when not with repeats?
    "Binary",
    "Ternary",
    "Rondo"


]


# SECTIONAL FORM STRUCTURES
SECTIONAL_FORM_STRUCTURES = {
    "Strophic": { # repeat same segment: AAAAAA
        "Variants": []
    },
    "Rondo": {
        "Variants": [
            "Symmetrical", # ABACABA
            "Asymmetrical" # ABACADAEA
        ]
    }
}



# Symmetrical: ABACABA
# Asymmetrical: ABACADAEA
def GetRondoPattern(symmetrical: bool):
    # try to solve constraints
    if symmetrical:
        return [0, 1, 0, 2, 0, 1, 0]
    else:
        return [0, 1, 0, 2, 0, 3, 0, 4, 0]




