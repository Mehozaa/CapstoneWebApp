import React from 'react';
import { SafeAreaView, StyleSheet, ImageBackground, Text, View } from 'react-native';
import { Radar } from 'react-chartjs-2';
import { Image } from 'react-native';
import 'chart.js/auto';

const Stats = ({ route }) => {
  const prediction = route.params?.prediction; 
  const averages = route.params?.averages; 
  const cumulativeStats = route.params?.cumulativeStats; 
  const position = route.params?.position; 
  const performanceCategories = route.params?.performanceCategories;
  const playerName = route.params?.playerName;
  const weektopredict = route.params?.weektopredict;
  const prediction2 = route.params?.prediction2;

  const featureSets = {
    'FW': ['goals', 'assists', 'shots_ontarget', 'chances2score', 'drib_success'],
    'DF': ['clearances', 'interceptions', 'tackles', 'aerials_w', 'dribbled_past'],
    'MF': ['keypasses', 'touches', 'passes_acc', 'lballs_acc', 'interceptions'],
    'GK': ['saves_itb', 'saves_otb', 'stop_shots', 'saved_pen', 'goals_ag_itb', 'goals_ag_otb']
  };
  const getCategoryColor = (category) => {
    switch (category) {
      case 'High':
        return 'green';
      case 'Medium':
        return 'orange';
      case 'Low':
        return 'red';
      default:
        return 'black'; 
    }
  };

  const options = {
    scales: {
      r: {
        angleLines: {
          display: false
        },
        suggestedMin: 0,
        ticks: {
          beginAtZero: true,
          backdropColor: 'transparent',
          color: '#FFFFFF', 
          font: {
            size: 12, 
          },
        },
        pointLabels: {
          font: {
            size: 14, 
            weight: 'bold', 
          },
          color: '#FFFFFF', 
        },
        grid: {
          color: '#FFFFFF', 
          borderWidth: 2, 
        },
      },
    },
    plugins: {
      legend: {
        labels: {
          font: {
            size: 16, 
          },
          color: '#FFFFFF', 
        },
      },
    },
    maintainAspectRatio: false,
    responsive: true,
  };
  
  const renderPredictionRow = (label, value) => (
    <View style={styles.predictionRow}>
      <Text style={styles.predictionLabel}>{label}</Text>
      <Text style={styles.predictionValue}>{value.toFixed(2)}</Text>
    </View>
  );

  const prepareRadarChartData = () => {
    if (!cumulativeStats || !position || !featureSets[position]) {
      return null;
    }

    const labels = featureSets[position];
    const data = labels.map(label => cumulativeStats[label] || 0);
   
    return {
      labels,
      datasets: [{
        label: `${position} Cumulative Stats`,
        data: data,
        backgroundColor: 'rgba(0, 255, 255, 0.2)',
        borderColor: 'rgba(0, 255, 255, 1)',
        borderWidth: 1,
      }],
    };
  }

  const renderTableHeader = () => (
    <View style={styles.tableRow}>
      <Text style={styles.tableHeader}>Feature</Text>
      <Text style={styles.tableHeader}>Average</Text>
    </View>
  );

  const renderTableRow = (feature, average) => {
    const category = performanceCategories[feature];
    const textColor = getCategoryColor(category);
  
    return (
      <View key={feature} style={styles.tableRow}>
        <Text style={styles.tableCell}>{feature}</Text> {}
        <Text style={[styles.tableCell, { color: textColor }]}>{average.toFixed(2)}</Text> {}
      </View>
    );
  };
  const renderTableRows = () => {
    if (!averages || !position || !featureSets[position]) return null;

    return Object.entries(averages)
      .filter(([feature, _]) => featureSets[position].includes(feature))
      .map(([feature, average]) => renderTableRow(feature, average));
  };

  const radarChartData = prepareRadarChartData();

  return (
    <SafeAreaView style={styles.container}>
      <ImageBackground 
        source={require('./logo4.png')} 
        style={styles.backgroundImage}
        resizeMode='cover'
      >
        <View style={styles.playerDetails}>
          <Text style={styles.detailText}>Player: {playerName}</Text>
          <Text style={styles.detailText}> | Position: {position}</Text>
          <Text style={styles.detailText}> | Week: {weektopredict}</Text>
        </View>
        {}
        <View style={styles.chartTopLeft}>
          {radarChartData && (
            <Radar
              data={radarChartData}
              options={options}
              width={300} 
              height={300} 
            />
          )}
        </View>

        {}
        <View style={styles.tableTopRight}>
          {averages && (
            <>
              {renderTableHeader()}
              {renderTableRows()}
            </>
          )}
        </View>

        <View style={styles.centeredView}>
          <Image
            source={require('./player.png')}
            style={styles.playerImage}
          />
        <View style={styles.predictionsView}>
          {prediction && renderPredictionRow('Prediction 1', prediction)}
          {prediction2 && renderPredictionRow('Prediction 2', prediction2)}
        </View>
          {}

        </View>
      </ImageBackground>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212', 
  },
  backgroundImage: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    resizeMode: 'cover',
    opacity: 0.95, 
    background: 'linear-gradient(180deg, #0D47A1 0%, #1976D2 100%)', 
  },
  chartTopLeft: {
    position: 'absolute',
    top: 130,
    left: 30,
    width: '36%',
    height: '50%',
    backgroundColor: 'rgba(13, 71, 161, 0.4)', 
    borderRadius: 20,
    padding: 15,
    boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.5)',
  },
  tableTopRight: {
    position: 'absolute',
    top: 130,
    right: 30,
    width: '36%',
    height: '50%',
    backgroundColor: 'rgba(13, 71, 161, 0.4)', 
    borderRadius: 20,
    padding: 15,
    boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.5)',
  },
  centeredView: {
    justifyContent: 'center',
    alignItems: 'center',
    position: 'absolute',
    left: '50%',
    top: '41%',
    transform: 'translate(-50%, -50%)',
    width: 300,
    height: 420,
  },
  predictionText: {
    backgroundColor: 'rgba(13, 71, 161, 0.4)', 
    fontSize: 26,
    fontWeight: 'bold',
    color: '#CDDC39', 
    marginTop: 10,
    textShadow: '0px 4px 4px rgba(0, 0, 0, 0.5)',
  },
  tableRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 20,
    paddingHorizontal: 15,
    borderBottomWidth: 1,
    borderColor: '#B0BEC5', 
  },
  tableHeader: {
    fontWeight: 'bold',
    fontSize: 18,
    color: '#FFFFFF', 
    marginBottom: 5,
  },
  tableCell: {
    fontWeight: 'bold',
    fontSize: 16,
    color: '#ECEFF1', 
  },
  playerImage: {
    width: '100%',
    height: '100%',
    resizeMode: 'cover',
    borderRadius: 50,
    borderColor: 'rgba(255, 215, 0, 0.6)', 
    borderWidth: 3,
    boxShadow: '0px 4px 8px rgba(255, 235, 59, 0.5)', 
  },
  playerDetails: {
    position: 'absolute', 
    top: 0,
    left: 0, 
    right: 0, 
    flexDirection: 'row', 
    justifyContent: 'center', 
    alignItems: 'center', 
    marginTop: 20, 
    padding: 10, 
    backgroundColor: 'transparent', 
  },
  detailText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FFF', 
    marginHorizontal: 5, 
  },
  predictionsView: {
    position: 'absolute',
    top: '120%', 
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: '80%',
    height: '30%',
    backgroundColor: 'rgba(13, 71, 161, 0.4)', 
    borderRadius: 20,
    padding: 15,
    boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.5)',
  },
  predictionRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 10,
    paddingHorizontal: 15,
    borderBottomWidth: 1,
    borderColor: '#B0BEC5',
  },
  predictionLabel: {
    fontWeight: 'bold',
    fontSize: 16,
    color: '#FFFFFF',
  },
  predictionValue: {
    fontWeight: 'bold',
    fontSize: 16,
    color: '#ECEFF1',
  },
});

export default Stats;

