from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)
CORS(app)

model = RandomForestRegressor()
print("RandomForestRegressor instance created:", model)
model2 = joblib.load('C:\\Users\\pc\\OneDrive - Al Akhawayn University in Ifrane\\Desktop\\capstone data\\trained_model2.pkl')
scaler2 = joblib.load('C:\\Users\\pc\\OneDrive - Al Akhawayn University in Ifrane\\Desktop\\capstone data\\trained_scaler2.pkl')

def categorize_performance(averages, data, week):
    week = int(week)
    week_data = data[data['week'] < week]
    categorized_performance = {}

    for feature, average in averages.items():
        feature_data = week_data[feature]
        low_threshold = feature_data.quantile(0.25)
        high_threshold = feature_data.quantile(0.75)

        if average <= low_threshold:
            category = 'Low'
        elif average >= high_threshold:
            category = 'High'
        else:
            category = 'Medium'

        categorized_performance[feature] = category

    return categorized_performance


features = [
    'goals',
    'assists',
    'shots_ontarget',
    'shots_offtarget',
    'shotsblocked',
    'chances2score',
    'drib_success',
    'drib_unsuccess',
    'keypasses',
    'touches',
    'passes_acc',
    'passes_inacc',
    'crosses_acc',
    'crosses_inacc',
    'lballs_acc',
    'lballs_inacc',
    'grduels_w',
    'grduels_l',
    'aerials_w',
    'aerials_l',
    'poss_lost',
    'fouls',
    'wasfouled',
    'clearances',
    'stop_shots',
    'interceptions',
    'tackles',
    'ycards',
    'rcards',
    'dangmistakes',
    'countattack',
    'offsides',
    'goals_ag_otb',
    'goals_ag_itb',
    'saves_itb',
    'saves_otb',
    'saved_pen',
    'missed_penalties',
    'owngoals',
    'win',
    'lost',
    'minutesPlayed',
    'game_duration'
]







def predict_player_rating_up_to_week2(file_path, player_name, week, model2, scaler2 , features):

    data = pd.read_csv(file_path)

    if not set(features).issubset(data.columns):
        return "Required features not available in the dataset."

    data_player = data[(data['player'] == player_name) & (data['week'] < week)].copy()

    if data_player.empty:
        return "Data not available for the specified player."

    if data_player[features].isnull().values.any():
        return "Missing data in the required features."

    recent_data = data_player.tail(1)

    X_standardized = scaler2.transform(recent_data[features])

    predicted_rating2 = model2.predict(X_standardized)

    return predicted_rating2[0]







pos_fw_weights = {
    'original_rating': 1,
    'goals': 1.5,
    'assists': 1.25,
    'shots_ontarget': 1.25,
    'shots_offtarget': 1,
    'shotsblocked': 0.5,
    'chances2score': 1.25,
    'drib_success': 1,
    'drib_unsuccess': 0.5,
    'keypasses': 1,
    'touches': 0.75,
    'passes_acc': 0.75,
    'passes_inacc': 0.5,
    'crosses_acc': 0.75,
    'crosses_inacc': 0.5,
    'lballs_acc': 0.75,
    'lballs_inacc': 0.5,
    'grduels_w': 0.5,
    'grduels_l': 0.5,
    'aerials_w': 0.5,
    'aerials_l': 0.5,
    'poss_lost': 0.75,
    'fouls': 0.5,
    'wasfouled': 0.75,
    'clearances': 0.25,
    'stop_shots': 0.25,
    'interceptions': 0.25,
    'tackles': 0.25,
    'ycards': 0.5,
    'rcards': 0.5,
    'dangmistakes': 1,
    'countattack': 1,
    'offsides': 0.75,
    'goals_ag_otb': 0.25,
    'goals_ag_itb': 0.25,
    'saves_itb': 0,
    'saves_otb': 0,
    'saved_pen': 0,
    'missed_penalties': 1,
    'owngoals': 0.5,
    'win': 1,
    'lost': 1,
    'minutesPlayed': 1,
    'game_duration': 0.5
}



pos_mf_weights = {
    'original_rating': 1,
    'goals': 0.75,
    'assists': 1.25,
    'shots_ontarget': 0.75,
    'shots_offtarget': 0.5,
    'shotsblocked': 0.5,
    'chances2score': 0.75,
    'drib_success': 0.75,
    'drib_unsuccess': 0.5,
    'keypasses': 1.25,
    'touches': 1,
    'passes_acc': 1.25,
    'passes_inacc': 0.75,
    'crosses_acc': 1,
    'crosses_inacc': 0.75,
    'lballs_acc': 1,
    'lballs_inacc': 0.75,
    'grduels_w': 0.75,
    'grduels_l': 0.75,
    'aerials_w': 0.5,
    'aerials_l': 0.5,
    'poss_lost': 1,
    'fouls': 0.75,
    'wasfouled': 0.75,
    'clearances': 0.5,
    'stop_shots': 0.5,
    'interceptions': 1,
    'tackles': 1,
    'ycards': 0.75,
    'rcards': 0.75,
    'dangmistakes': 1,
    'countattack': 0.75,
    'offsides': 0.5,
    'goals_ag_otb': 0.5,
    'goals_ag_itb': 0.25,
    'saves_itb': 0,
    'saves_otb': 0,
    'saved_pen': 0,
    'missed_penalties': 0.75,
    'owngoals': 0.5,
    'win': 1,
    'lost': 1,
    'minutesPlayed': 1,
    'game_duration': 0.5
}

pos_gk_weights = {
    'original_rating': 1,
    'goals': 0,
    'assists': 0,
    'shots_ontarget': 0,
    'shots_offtarget': 0,
    'shotsblocked': 0.75,
    'chances2score': 0,
    'drib_success': 0,
    'drib_unsuccess': 0,
    'keypasses': 0.5,
    'touches': 1,
    'passes_acc': 1,
    'passes_inacc': 0.75,
    'crosses_acc': 0,
    'crosses_inacc': 0,
    'lballs_acc': 1,
    'lballs_inacc': 0.5,
    'grduels_w': 0,
    'grduels_l': 0,
    'aerials_w': 0.75,
    'aerials_l': 0.75,
    'poss_lost': 0.75,
    'fouls': 0.5,
    'wasfouled': 0.5,
    'clearances': 1,
    'stop_shots': 1.5,
    'interceptions': 0.5,
    'tackles': 0,
    'ycards': 0.5,
    'rcards': 0.5,
    'dangmistakes': 1,
    'countattack': 0,
    'offsides': 0,
    'goals_ag_otb': 1.25,
    'goals_ag_itb': 1.5,
    'saves_itb': 1.5,
    'saves_otb': 1.5,
    'saved_pen': 1.5,
    'missed_penalties': 0,
    'owngoals': 0.5,
    'win': 1,
    'lost': 1,
    'minutesPlayed': 1,
    'game_duration': 0.5
}


pos_sub_weights = {
    'original_rating': 1,
    'goals': 1,
    'assists': 1,
    'shots_ontarget': 1,
    'shots_offtarget': 1,
    'shotsblocked': 1,
    'chances2score': 1,
    'drib_success': 1,
    'drib_unsuccess': 1,
    'keypasses': 1,
    'touches': 1,
    'passes_acc': 1,
    'passes_inacc': 1,
    'crosses_acc': 1,
    'crosses_inacc': 1,
    'lballs_acc': 1,
    'lballs_inacc': 1,
    'grduels_w': 1,
    'grduels_l': 1,
    'aerials_w': 1,
    'aerials_l': 1,
    'poss_lost': 1,
    'fouls': 1,
    'wasfouled': 1,
    'clearances': 11,
    'stop_shots': 1,
    'interceptions': 1,
    'tackles': 1,
    'ycards': 1,
    'rcards': 1,
    'dangmistakes': 1,
    'countattack': 1,
    'offsides': 1,
    'goals_ag_otb': 1,
    'goals_ag_itb': 1,
    'saves_itb': 0,
    'saves_otb': 0,
    'saved_pen': 0,
    'missed_penalties': 1,
    'owngoals': 1,
    'win': 1,
    'lost': 1,
    'minutesPlayed': 1,
    'game_duration': 1
}
pos_df_weights = {
    'original_rating': 1,
    'goals': 0.5,
    'assists': 0.5,
    'shots_ontarget': 0.25,
    'shots_offtarget': 0.25,
    'shotsblocked': 1.25,
    'chances2score': 0.25,
    'drib_success': 0.25,
    'drib_unsuccess': 0.25,
    'keypasses': 0.5,
    'touches': 1,
    'passes_acc': 1,
    'passes_inacc': 0.75,
    'crosses_acc': 0.5,
    'crosses_inacc': 0.5,
    'lballs_acc': 1,
    'lballs_inacc': 0.5,
    'grduels_w': 1.25,
    'grduels_l': 1.25,
    'aerials_w': 1.25,
    'aerials_l': 1.25,
    'poss_lost': 1,
    'fouls': 0.75,
    'wasfouled': 0.75,
    'clearances': 1.5,
    'stop_shots': 1,
    'interceptions': 1.25,
    'tackles': 1.25,
    'ycards': 0.75,
    'rcards': 0.75,
    'dangmistakes': 0.75,
    'countattack': 0.75,
    'offsides': 0.25,
    'goals_ag_otb': 0.75,
    'goals_ag_itb': 1,
    'saves_itb': 0,
    'saves_otb': 0,
    'saved_pen': 0,
    'missed_penalties': 0.5,
    'owngoals': 0.75,
    'win': 1,
    'lost': 1,
    'minutesPlayed': 1,
    'game_duration': 0.5
}

def apply_positional_weighting(row, features, pos_column, weight_dict):
    for feature in features:
        row[feature] = row[feature] * weight_dict.get(feature, 1) if row[pos_column] == 1 else row[feature]
    return row







def predict_player_rating_up_to_week(file_path, player_name, week, model):
    data = pd.read_csv(file_path)
    relevant_columns = ['week', 'player', 'original_rating'] + [col for col in data.columns if 'pos_role' in col]
    data_ml = data[relevant_columns].copy()

    week = int(week)
    data_player = data_ml[(data_ml['player'] == player_name) & (data_ml['week'] < week)].copy()
    
    if data_player.empty:
        return "Data not available for the specified player."

    for i in range(1, 35):
        data_player.loc[:, f'rating_lag_{i}'] = data_player['original_rating'].shift(i).fillna(0)

    X = data_player.drop(['week', 'player', 'original_rating'], axis=1)
    predicted_rating = model.predict(X.tail(1))
    return predicted_rating[0]

def calculate_cumulative_stats(file_path, player_name, week):
    try:
        data = pd.read_csv(file_path)
        week = int(week)
        data_player = data[(data['player'] == player_name) & (data['week'] <= week)]

        if data_player.empty:
            return "No data available for the specified player and week.", {}

        columns = {
            'FW': ['goals', 'assists', 'shots_ontarget', 'chances2score', 'drib_success'],
            'DF': ['clearances', 'interceptions', 'tackles', 'aerials_w', 'dribbled_past'],
            'MF': ['keypasses', 'touches', 'passes_acc', 'lballs_acc', 'interceptions'],
            'GK': ['saves_itb', 'saves_otb', 'stop_shots', 'saved_pen', 'goals_ag_itb', 'goals_ag_otb']
        }

        latest_data = data_player.iloc[-1]
        player_position = None
        for position in ['FW', 'DF', 'MF', 'GK']:
            if latest_data.get(f'pos_{position}', 0) == 1:
                player_position = position
                break

        if not player_position:
            return f"No position data available for {player_name}.", {}

        features_to_cumulative = columns[player_position]
        cumulative_stats = data_player[features_to_cumulative].sum().to_dict()

        return cumulative_stats
    except Exception as e:
        return f"An error occurred: {e}", {}

def calculate_averages(file_path, player_name, week):
    try:
        data = pd.read_csv(file_path)
        week = int(week)
        data_player = data[(data['player'] == player_name) & (data['week'] < week)]

        if data_player.empty:
            return "No data available for the specified player and week.", {}

        columns = {
            'FW': ['goals', 'assists', 'shots_ontarget', 'chances2score', 'drib_success'],
            'DF': ['clearances', 'interceptions', 'tackles', 'aerials_w', 'dribbled_past'],
            'MF': ['keypasses', 'touches', 'passes_acc', 'lballs_acc', 'interceptions'],
            'GK': ['saves_itb', 'saves_otb', 'stop_shots', 'saved_pen', 'goals_ag_itb', 'goals_ag_otb']
        }

        latest_data = data_player.iloc[-1]
        player_position = None
        for position in ['FW', 'DF', 'MF', 'GK']:
            if latest_data.get(f'pos_{position}', 0) == 1:
                player_position = position
                break

        if not player_position:
            return f"No position data available for {player_name}.", {}

        features_to_average = columns[player_position]
        averages = data_player[features_to_average].mean().to_dict()

        return averages
    except Exception as e:
        return f"An error occurred: {e}", {}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    player_name = data.get('playerName')
    week = int(data.get('weektopredict'))

    file_path = 'C:\\Users\\pc\\OneDrive - Al Akhawayn University in Ifrane\\Desktop\\capstone data\\finally imken2222.csv'
    full_data = pd.read_csv(file_path)
    
    predicted_rating = predict_player_rating_up_to_week(file_path, player_name, week, model)
    averages = calculate_averages(file_path, player_name, week)
    cumulative_stats = calculate_cumulative_stats(file_path, player_name, week)
    performance_categories = categorize_performance(averages, full_data, week)
    predicted_rating2 = predict_player_rating_up_to_week2(file_path, player_name, week, model2, scaler2, features)
    response_data = {
        'prediction': predicted_rating,
        'averages': averages,
        'cumulativeStats': cumulative_stats,
        'performanceCategories': performance_categories,
        'prediction2': predicted_rating2
    }

    response = make_response(jsonify(response_data))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

model = joblib.load('C:\\Users\\pc\\OneDrive - Al Akhawayn University in Ifrane\\Desktop\\capstone data\\trained_model.pkl')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
