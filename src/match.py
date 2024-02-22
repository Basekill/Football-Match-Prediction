from dataclasses import dataclass
from src.match_stats import MatchStats
from src.match_event import MatchEvent, EventType, CardType
from enum import Enum
from typing import Dict, List
from copy import deepcopy
import pandas as pd


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

def goal_timings_to_list(goal_timings: str):
  if pd.isna(goal_timings):
    return []
  return list(map(int, goal_timings.split(',')))

def goal_timings_to_str(goal_timings: List[int]):
  return ','.join(map(str, goal_timings))

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
  status: MatchStatus = MatchStatus.FIRST_HALF

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
    match event.event_type:
      case (EventType.HALF_TIME, EventType.FULL_TIME):
        self.home_team_stats.process_event(event)
        self.away_team_stats.process_event(event)
      case _:
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
  
  def from_dataframe(df):
    home_team_stats = TeamStats(
      team_name=df['home_team_name'],
      goal_count=df['home_team_goal_count'],
      goal_count_half_time=df['home_team_goal_count_half_time'],
      goal_timings=goal_timings_to_list(df['home_team_goal_timings']),
      corner_count=df['home_team_corner_count'],
      yellow_cards=df['home_team_yellow_cards'],
      red_cards=df['home_team_red_cards'],
      first_half_cards=df['home_team_first_half_cards'],
      second_half_cards=df['home_team_second_half_cards'],
      shots=df['home_team_shots'],
      shots_on_target=df['home_team_shots_on_target'],
      shots_off_target=df['home_team_shots_off_target'],
      fouls=df['home_team_fouls'],
      possession=df['home_team_possession'],
      status=MatchStatus.from_str(df['status'])
    )

    away_team_stats = TeamStats(
      team_name=df['away_team_name'],
      goal_count=df['away_team_goal_count'],
      goal_count_half_time=df['away_team_goal_count_half_time'],
      goal_timings=goal_timings_to_list(df['away_team_goal_timings']),
      corner_count=df['away_team_corner_count'],
      yellow_cards=df['away_team_yellow_cards'],
      red_cards=df['away_team_red_cards'],
      first_half_cards=df['away_team_first_half_cards'],
      second_half_cards=df['away_team_second_half_cards'],
      shots=df['away_team_shots'],
      shots_on_target=df['away_team_shots_on_target'],
      shots_off_target=df['away_team_shots_off_target'],
      fouls=df['away_team_fouls'],
      possession=df['away_team_possession'],
      status=MatchStatus.from_str(df['status'])
    )

    match_stats = MatchStats(
      home_team_stats=home_team_stats,
      away_team_stats=away_team_stats
    )

    return match_stats
  
  def to_dataframe(self):
    return pd.DataFrame({
      'home_team_name': self.home_team_stats.team_name,
      'home_team_goal_count': self.home_team_stats.goal_count,
      'home_team_goal_count_half_time': self.home_team_stats.goal_count_half_time,
      'home_team_goal_timings': goal_timings_to_str(self.home_team_stats.goal_timings),
      'home_team_corner_count': self.home_team_stats.corner_count,
      'home_team_yellow_cards': self.home_team_stats.yellow_cards,
      'home_team_red_cards': self.home_team_stats.red_cards,
      'home_team_first_half_cards': self.home_team_stats.first_half_cards,
      'home_team_second_half_cards': self.home_team_stats.second_half_cards,
      'home_team_shots': self.home_team_stats.shots,
      'home_team_shots_on_target': self.home_team_stats.shots_on_target,
      'home_team_shots_off_target': self.home_team_stats.shots_off_target,
      'home_team_fouls': self.home_team_stats.fouls,
      'home_team_possession': self.home_team_stats.possession,
      'away_team_name': self.away_team_stats.team_name,
      'away_team_goal_count': self.away_team_stats.goal_count,
      'away_team_goal_count_half_time': self.away_team_stats.goal_count_half_time,
      'away_team_goal_timings': goal_timings_to_str(self.away_team_stats.goal_timings),
      'away_team_corner_count': self.away_team_stats.corner_count,
      'away_team_yellow_cards': self.away_team_stats.yellow_cards,
      'away_team_red_cards': self.away_team_stats.red_cards,
      'away_team_first_half_cards': self.away_team_stats.first_half_cards,
      'away_team_second_half_cards': self.away_team_stats.second_half_cards,
      'away_team_shots': self.away_team_stats.shots,
      'away_team_shots_on_target': self.away_team_stats.shots_on_target,
      'away_team_shots_off_target': self.away_team_stats.shots_off_target,
      'away_team_fouls': self.away_team_stats.fouls,
      'away_team_possession': self.away_team_stats.possession
    })



  
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
