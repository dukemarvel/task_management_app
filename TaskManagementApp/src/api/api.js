import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const api = axios.create({
    baseURL: 'http://192.168.43.199:5000/api/v1', 
});


api.interceptors.request.use(
    async (config) => {
        try {
            console.log("getting access_token")
            const token = await AsyncStorage.getItem('access_token');

            console.log("Got accessed token ", token)
            if (token) {
                config.headers['Authorization'] = `Bearer ${token}`;
            }

            return config;
        } catch (error) {
            console.error('Error retrieving access token', error);
            return Promise.reject(error);
        }
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default api;
