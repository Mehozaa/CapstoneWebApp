
import React, { useState } from 'react';
import { SafeAreaView, StyleSheet, ImageBackground, View, Text, Image, TextInput, Button } from 'react-native';

const Home = (props) => { 
  const [playerName, setPlayerName] = useState('');
  const [playerPosition, setPosition] = useState('');
  const [weektopredict, setWeek] = useState('');

  const handlePress = async () => {
    props.navigation.navigate('Stats'); 
  
    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          playerName: playerName,
          weektopredict: parseInt(weektopredict, 10)
          
        }),
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const result = await response.json();
      
      props.navigation.navigate('Stats', { prediction: result.prediction, averages: result.averages, position: playerPosition, cumulativeStats: result.cumulativeStats,  performanceCategories: result.performanceCategories,   playerName: playerName,
        weektopredict: weektopredict, prediction2: result.prediction2});
    } catch (error) {
      console.error('There was an error fetching the prediction:', error);
    }
  };
  return (
    <SafeAreaView style={styles.container}>
      <ImageBackground
        source={{ uri: 'https://t4.ftcdn.net/jpg/01/09/56/69/360_F_109566993_Yg7AXTaRhWt2oOaHiXCAmnhtYeAd9VjY.jpg' }}
        style={styles.backgroundImage}
      >
        <View style={styles.contentContainer}>
          <View style={styles.messageContainer}>
            <Text style={styles.welcomeMessage}>
              Welcome to the Ultimate Player Stats Tracker!
            </Text>
            <Text style={styles.subMessage}>
              Discover and explore the amazing world of sports statistics.
            </Text>
            <TextInput
              style={styles.input}
              onChangeText={setPlayerName}
              value={playerName}
              placeholder="Enter Player Name"
              placeholderTextColor="#999"
            />
            <TextInput
              style={styles.input}
              onChangeText={setPosition}
              value={playerPosition}
              placeholder="Enter The Position (FW, DF, MF or GK)"
              placeholderTextColor="#999"
            />
            <TextInput
              style={styles.input}
              onChangeText={setWeek}
              value={weektopredict}
              placeholder="Enter The Week to Predict"
              placeholderTextColor="#999"
            />
            <View style={styles.button}>
              <Button
                title="Go to Player Stats"
                onPress={handlePress}
              />
            </View>
          </View>
          <Image
            source={require('./logo.png')}
            style={styles.imageStyle}
          />
        </View>
      </ImageBackground>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  backgroundImage: {
    flex: 1,
    justifyContent: 'center', 
  },
  contentContainer: {
    flex: 1,
    flexDirection: 'row', 
    alignItems: 'center', 
    justifyContent: 'center', 
  },
  messageContainer: {
    flex: 1, 
    justifyContent: 'center',
    alignItems: 'flex-start', 
    paddingLeft: 20, 
    width: '100%', 
  },
  welcomeMessage: {
    fontSize: 62, 
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 30, 
    textAlign: 'center',
    fontFamily: 'Helvetica Neue', 
    marginLeft: 60,
  },

  input: {
    width: 500,
    height: 50, 
    marginVertical: 10, 
    marginHorizontal: 20,
    marginLeft: 250, 
    borderWidth: 1,
    alignItems: 'center',
    borderColor: '#ffffff', 
    padding: 15,
    backgroundColor: 'white',
    borderRadius: 10, 
    fontSize: 16, 
    fontFamily: 'Helvetica Neue',
  },
  button: {
    backgroundColor: '#2089dc', 
    padding: 15,
    borderRadius: 15, 
    alignSelf: 'center', 
    paddingHorizontal: 20, 
    paddingVertical: 20, 
    marginTop: 10,
    marginLeft: 80,

  },
  buttonText: {
    backgroundColor: '#2089dc',
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
    fontFamily: 'Helvetica Neue',
  },
  imageStyle: {
    flex: 1, 
    width: '50%%', 
    height: '70%', 
    resizeMode: 'contain', 
  },

});


export default Home;
