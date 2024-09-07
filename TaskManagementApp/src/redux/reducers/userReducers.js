const initialState = {
    isAuthenticated: false,
    token: null,
    error: null,
};

const userReducer = (state = initialState, action) => {
    switch (action.type) {
        case 'LOGIN_SUCCESS':
            console.log('Login successful, updating state with token:', action.payload);
            return {
                ...state,
                isAuthenticated: true,
                token: action.payload,
                error: null,
            };
        case 'LOGIN_FAILURE':
            console.log('Login failed with error:', action.payload);
            return {
                ...state,
                error: action.payload,
            };
        case 'REGISTER_SUCCESS':
            return {
                ...state,
                error: null,
            };
        case 'REGISTER_FAILURE':
            return {
                ...state,
                error: action.payload,
            };
        case 'LOGOUT':
            return {
                ...state,
                isAuthenticated: false,
                token: null,
            };
        default:
            return state;
    }
};

export default userReducer;
