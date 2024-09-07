import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
import { useDispatch } from 'react-redux';
import { login, register } from '../redux/actions/userActions';
import { useNavigation } from '@react-navigation/native';

const UserScreen = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const [isRegistering, setIsRegistering] = useState(false);
    const dispatch = useDispatch();
    const navigation = useNavigation();

    const handleLogin = async () => {
        console.log('Login button pressed');
        try {
            const loginData = { username: email, password };
            console.log('Dispatching login action with data:', loginData);
            await dispatch(login(loginData));
            console.log('Login successful, navigating to TaskList');
            navigation.navigate('TaskList');
        } catch (error) {
            console.error('Login Error:', error.message);
            Alert.alert('Login Error', error.message || 'Invalid credentials');
        }
    };
    
    
    
    const handleRegister = async () => {
        console.log('Register button pressed'); 
        try {
            const userData = { email, password, full_name: fullName };
            await dispatch(register(userData));
            Alert.alert('Success', 'User registered successfully!');
            navigation.navigate('TaskList');
        } catch (error) {
            console.error('Registration Error:', error);
            Alert.alert('Registration Error', error.message || 'Something went wrong');
        }
    };
    

    return (
        <View>
            {isRegistering && (
                <TextInput
                    value={fullName}
                    onChangeText={setFullName}
                    placeholder="Full Name"
                />
            )}
            <TextInput
                value={email}
                onChangeText={setEmail}
                placeholder="Email"
                keyboardType="email-address"
            />
            <TextInput
                value={password}
                onChangeText={setPassword}
                placeholder="Password"
                secureTextEntry
            />
            <Button
                title={isRegistering ? "Register" : "Login"}
                onPress={isRegistering ? handleRegister : handleLogin}
            />
            <Button
                title={isRegistering ? "Already have an account? Login" : "Don't have an account? Register"}
                onPress={() => setIsRegistering(!isRegistering)}
            />
        </View>
    );
};

export default UserScreen;
