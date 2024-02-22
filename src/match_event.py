from dataclasses import dataclass
from enum import Enum

class TeamSide(Enum):
  HOME = 1
  AWAY = 2

class EventType(Enum):
  GOAL = 1
  SHOT = 2
  CORNER = 3
  POSSESSION = 4
  YELLOW_CARD = 5
  RED_CARD = 6
  HALF_TIME = 7
  FULL_TIME = 8

@dataclass
class MatchEvent:
  event_type: EventType
  team_side: TeamSide
  time: int

@dataclass
class Shot(MatchEvent):
  on_target: bool
