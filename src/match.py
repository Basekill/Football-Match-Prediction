from dataclasses import dataclass
from src.match_stats import MatchStats
from src.match_event import MatchEvent, EventType, CardType
from enum import Enum
from typing import Dict, List
from copy import deepcopy

class TeamSide(Enum):
  HOME = 1
  AWAY = 2

class MatchStatus(Enum):
  FIRST_HALF = 1
  SECOND_HALF = 2
  COMPLETE = 3

@dataclass
class TeamStats:
  team_name: str
  goal_count: int = 0
  goal_count_half_time: int = 0
  goal_timings: List[int] = []
  corner_count: int = 0
  yellow_cards: int = 0
  red_cards: int = 0
  first_half_cards: int = 0
  second_half_cards: int = 0
  shots: int = 0
  shots_on_target: int = 0
  shots_off_target: int = 0
  fouls: int = 0
  possession: int = 50
  match_status: MatchStatus = MatchStatus.FIRST_HALF

  # pre_match_xg: float
  # xg: float
  # pre_match_ppg: float
  # ppg: float
  # average_goals_per_match_pre_match: float
  # average_corners_per_match_pre_match: float
  # average_cards_per_match_pre_match: float

  def process_event(self, event: MatchEvent):
    match event.event_type:
      case EventType.GOAL:
        self.process_goal(event)
      case EventType.SHOT:
        self.process_shot(event)
      case EventType.CORNER:
        self.process_corner(event)
      case EventType.POSSESSION:
        self.process_possession(event)
      case EventType.CARD:
        self.process_card(event)
      case EventType.HALF_TIME:
        self.process_half_time(event)
      case EventType.FULL_TIME:
        self.process_full_time(event)

  def process_goal(self, event: MatchEvent):
    self.goal_count += 1
    self.goal_timings.append(event.time)

    if self.match_status == MatchStatus.FIRST_HALF:
      self.goal_count_half_time += 1
  
  def process_shot(self, event: MatchEvent):
    self.shots += 1
    if event.on_target:
      self.shots_on_target += 1
    else:
      self.shots_off_target += 1
  
  def process_corner(self, event: MatchEvent):
    self.corner_count += 1
  
  def process_possession(self, event: MatchEvent):
    self.possession = event.possession_percentage
  
  def process_card(self, event: MatchEvent):
    match event.card_type:
      case CardType.YELLOW:
        self.yellow_cards += 1
      case CardType.RED:
        self.red_cards += 1

    if self.match_status == MatchStatus.FIRST_HALF:
      self.first_half_cards += 1
    else:
      self.second_half_cards += 1
  
  def process_half_time(self, event: MatchEvent):
    self.match_status = MatchStatus.SECOND_HALF
  
  def process_full_time(self, event: MatchEvent):
    self.match_status = MatchStatus.COMPLETE


@dataclass
class MatchStats:
  home_team_stats: TeamStats
  away_team_stats: TeamStats

  def process_event(self, event: MatchEvent):
    match event.team_side:
      case TeamSide.HOME:
        self.home_team_stats.process_event(event)
      case TeamSide.AWAY:
        self.away_team_stats.process_event(event)
  
  @property
  def total_goal_count(self):
    return self.home_team_stats.goal_count + self.away_team_stats.goal_count
  
  @property
  def total_goals_at_half_time(self):
    return self.home_team_stats.goal_count_half_time + self.away_team_stats.goal_count_half_time
  
class Match:
  match_events: Dict[int, List[MatchEvent]]
  match_stats : Dict[int, List[MatchStats]]

  def __init__(self):
    self.match_events = {}
    self.match_stats = {}

  def process_event(self, event: MatchEvent):
    stats = deepcopy(self.match_stats[-1])
    stats.process_event(event)
    self.match_events[event.time].append(event)
    self.match_stats[event.time] = stats
  
  def simulate(self, events: List[MatchEvent]):
    for event in events:
      self.process_event(event)
