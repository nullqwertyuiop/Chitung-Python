from enum import Enum


class Waters(Enum):
    Amur = 1  # A
    Caroline = 2  # B
    Chishima = 3  # C
    General = 4


class Time(Enum):
    Day = "Day"
    Night = "Night"
    All = "All"
