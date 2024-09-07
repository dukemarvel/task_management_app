import api from './api';
import AsyncStorage from '@react-native-async-storage/async-storage';
import qs from 'qs';

export const loginUser = async (loginData) => {
    try {
        console.log('Sending login request(next log should show whether it is a success or failure):', loginData);
        const response = await api.post('/login', qs.stringify(loginData), {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });
        console.log('Login response Success or Failure:', response.data);
        
        const { access_token } = response.data;
        await AsyncStorage.setItem('access_token', access_token);
        
        return response.data;
    } catch (error) {
    
        if (error.response) {
            console.error('Error response data:', error.response.data);
            console.error('Error response status:', error.response.status);
            console.error('Error response headers:', error.response.headers);
        } else if (error.request) {
            console.error('No response received:', error.request);
        } else {
            console.error('Error in setting up request:', error.message);
        }
        throw error; 
    }
};


export const registerUser = async (userData) => {
    try {
        
        const response = await api.post('/register', userData, {
            headers: {
                'Content-Type': 'application/json',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error registering user', error.response?.data || error.message);
        throw error;
    }
};
