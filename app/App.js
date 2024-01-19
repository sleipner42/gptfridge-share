import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import PhotoView from './PhotoView.js';
import Ingredients from './Ingredients.js';
import Recipes from './Recipes.js';
import AddIngredients from './AddIngredient.js';
import 'react-native-gesture-handler';

const Stack = createStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="photo">
        <Stack.Screen name="Take Photos" component={PhotoView} />
        <Stack.Screen name="Your ingredients" component={Ingredients} />
        <Stack.Screen name="Recipes" component={Recipes} />
        <Stack.Screen name="AddIngredients" component={AddIngredients} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;