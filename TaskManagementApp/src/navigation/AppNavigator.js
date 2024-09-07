import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import TaskListScreen from '../screens/TaskListScreen';
import TaskFormScreen from '../screens/TaskFormScreen';
import UserScreen from '../screens/UserScreen';


const Stack = createStackNavigator();

function AppNavigator() {
    return (
        <NavigationContainer>
            <Stack.Navigator initialRouteName="User">
                <Stack.Screen name="User" component={UserScreen} />
                <Stack.Screen name="TaskList" component={TaskListScreen} />
                <Stack.Screen name="TaskForm" component={TaskFormScreen} />
            </Stack.Navigator>
        </NavigationContainer>
    );
}

export default AppNavigator;
