import { loginUser, registerUser } from '../../api/userApi';  

export const login = (loginData) => {
    return async (dispatch) => {
        try {
            console.log('Dispatching login request');
            const response = await loginUser(loginData);
            console.log('Dispatching LOGIN_SUCCESS with token:', response.access_token);
            dispatch({
                type: 'LOGIN_SUCCESS',
                payload: response.access_token,
            });
        } catch (error) {
            console.error('Error logging in:', error.message || error);
            dispatch({
                type: 'LOGIN_FAILURE',
                payload: error.message || 'Login failed',
            });
        }
    };
};


export const register = (userData) => {
    return async (dispatch) => {
        try {
            await registerUser(userData);
            dispatch({
                type: 'REGISTER_SUCCESS',
            });
        } catch (error) {
            console.error('Error registering', error);
            dispatch({
                type: 'REGISTER_FAILURE',
                payload: error.message,
            });
        }
    };
};

export const logout = () => ({
    type: 'LOGOUT',
});
