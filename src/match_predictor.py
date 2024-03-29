from joblib import load
from collections import namedtuple
from match import MatchStats

MatchPrediction = namedtuple('MatchPrediction', ['home_win', 'draw', 'away_win'])


class MatchPredictor:
  _instance = None

  def __new__(cls, *args, **kwargs):
    if not cls._instance:
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self, model_path: str = 'models/best_classifier.joblib'):
    if hasattr(self, 'model'):
      return
    self.model = load(model_path)

  def predict(self, match_stats: MatchStats) -> MatchPrediction:
    df = match_stats.to_dataframe()
    probabilities = self.model.predict_proba(df)
    match_prediction = MatchPrediction(
      away_win=probabilities[0][0],
      draw=probabilities[0][1],
      home_win=probabilities[0][2]
    )

    return match_prediction

