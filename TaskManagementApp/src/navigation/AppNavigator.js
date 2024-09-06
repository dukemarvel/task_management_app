import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import TaskListScreen from '../screens/TaskListScreen';
import TaskDetailScreen from '../screens/TaskDetailScreen';

const Stack = createStackNavigator();

function AppNavigator() {
    return (
        <NavigationContainer>
            <Stack.Navigator initialRouteName="TaskList">
                <Stack.Screen name="TaskList" component={TaskListScreen} />
                <Stack.Screen name="TaskDetail" component={TaskDetailScreen} />
            </Stack.Navigator>
        </NavigationContainer>
    );
}

export default AppNavigator;
