import streamlit as st
from match import Match, TeamStats, MatchStats
from match_enums import TeamSide
from match_event import MatchEvent, EventType, CardType, Shot, Possession, Card
from match_predictor import MatchPredictor

@st.cache_data
def predict_match_result(match_stats):
  match_predictor = MatchPredictor()
  match_prediction = match_predictor.predict(match_stats)
  return match_prediction


def main():

  # Create sliders for adjusting match stats
  col1, col2 = st.columns(2)

  with col1:
    st.write("Home Team")
    home_team_name = st.text_input("Team Name", key="home_team_name")
    # home_team_goal_count = st.slider("Goal Count", 0, 10, 0, key="home_goal_count")
    home_team_goal_count_half_time = st.slider("Goal Count at Half Time", 0, 10, 0, key="home_goal_count_half_time")
    home_team_corner_count = st.slider("Corner Count", 0, 20, 0, key="home_corner_count")
    home_team_yellow_cards = st.slider("Yellow Cards", 0, 10, 0, key="home_yellow_cards")
    home_team_red_cards = st.slider("Red Cards", 0, 5, 0, key="home_red_cards")
    home_team_first_half_cards = st.slider("First Half Cards", 0, 5, 0, key="home_first_half_cards")
    home_team_second_half_cards = st.slider("Second Half Cards", 0, 5, 0, key="home_second_half_cards")
    home_team_shots_on_target = st.slider("Shots on Target", 0, 50, 0, key="home_shots_on_target")
    home_team_shots_off_target = st.slider("Shots off Target", 0, 50, 0, key="home_shots_off_target")
    home_team_shots = home_team_shots_on_target + home_team_shots_off_target
    home_team_fouls = st.slider("Fouls", 0, 30, 0, key="home_fouls")

    with col2:
      st.write("Away Team")
      away_team_name = st.text_input("Team Name", key="away_team_name")
      # away_team_goal_count = st.slider("Goal Count", 0, 10, 0, key="away_goal_count")
      away_team_goal_count_half_time = st.slider("Goal Count at Half Time", 0, 10, 0, key="away_goal_count_half_time")
      away_team_corner_count = st.slider("Corner Count", 0, 20, 0, key="away_corner_count")
      away_team_yellow_cards = st.slider("Yellow Cards", 0, 10, 0, key="away_yellow_cards")
      away_team_red_cards = st.slider("Red Cards", 0, 5, 0, key="away_red_cards")
      away_team_first_half_cards = st.slider("First Half Cards", 0, 5, 0, key="away_first_half_cards")
      away_team_second_half_cards = st.slider("Second Half Cards", 0, 5, 0, key="away_second_half_cards")

      away_team_shots_on_target = st.slider("Shots on Target", 0, 50, 0, key="away_shots_on_target")
      away_team_shots_off_target = st.slider("Shots off Target", 0, 50, 0, key="away_shots_off_target")
      away_team_shots = away_team_shots_on_target + away_team_shots_off_target

      away_team_fouls = st.slider("Fouls", 0, 30, 0, key="away_fouls")

  home_team_possession = st.slider("Possession", 0, 100, 50, key="home_possession")
  away_team_possession = 100 - home_team_possession
  st.write(f"<div style='text-align: center;'>Home {home_team_possession}% - {away_team_possession}% Away</div>", unsafe_allow_html=True)
  
  home_team_stats = TeamStats(
    team_name=home_team_name,
    # goal_count=home_team_goal_count,
    goal_count_half_time=home_team_goal_count_half_time,
    corner_count=home_team_corner_count,
    yellow_cards=home_team_yellow_cards,
    red_cards=home_team_red_cards,
    first_half_cards=home_team_first_half_cards,
    second_half_cards=home_team_second_half_cards,
    shots=home_team_shots,
    shots_on_target=home_team_shots_on_target,
    shots_off_target=home_team_shots_off_target,
    fouls=home_team_fouls,
    possession=home_team_possession
  )

  away_team_stats = TeamStats(
    team_name=away_team_name,
    # goal_count=away_team_goal_count,
    goal_count_half_time=away_team_goal_count_half_time,
    corner_count=away_team_corner_count,
    yellow_cards=away_team_yellow_cards,
    red_cards=away_team_red_cards,
    first_half_cards=away_team_first_half_cards,
    second_half_cards=away_team_second_half_cards,
    shots=away_team_shots,
    shots_on_target=away_team_shots_on_target,
    shots_off_target=away_team_shots_off_target,
    fouls=away_team_fouls,
    possession=away_team_possession
  )

  match_stats = MatchStats(
    home_team_stats=home_team_stats,
    away_team_stats=away_team_stats
  )

  predict_button = st.button("Predict Match")

  if predict_button:
    # Predict match result
    match_prediction = predict_match_result(match_stats)

    st.write("Match Prediction:")
    chart_data = {
      'Home Win': match_prediction[0],
      'Draw': match_prediction[1],
      'Away Win': match_prediction[2]
    }
    st.bar_chart(chart_data)


# Run the main function
if __name__ == "__main__":
  main()