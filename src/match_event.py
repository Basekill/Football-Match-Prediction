from dataclasses import dataclass
from enum import Enum
from match_enums import TeamSide

class EventType(Enum):
  GOAL = 1
  SHOT = 2
  CORNER = 3
  POSSESSION = 4
  CARD = 5
  HALF_TIME = 6
  FULL_TIME = 7

@dataclass
class MatchEvent:
  event_type: EventType
  team_side: TeamSide
  time: int

@dataclass
class Shot(MatchEvent):
  on_target: bool

class CardType(Enum):
  YELLOW = 1
  RED = 2

@dataclass
class Card(MatchEvent):
  card_type: CardType

@dataclass
class Possession(MatchEvent):
  possession_percentage: int
