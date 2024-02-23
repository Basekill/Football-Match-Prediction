from enum import Enum

class TeamSide(Enum):
  HOME = 1
  AWAY = 2

class MatchStatus(Enum):
  FIRST_HALF = 1
  SECOND_HALF = 2
  COMPLETE = 3

  def __str__(self):
    return self.name.lower().replace('_', ' ')
  
  def from_str(status: str):
    return MatchStatus[status.upper().replace(' ', '_')]

