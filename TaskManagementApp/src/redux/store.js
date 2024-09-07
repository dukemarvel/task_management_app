import { configureStore } from '@reduxjs/toolkit';
import taskReducer from './reducers/taskReducers';
import userReducer from './reducers/userReducers';  

const store = configureStore({
    reducer: {
        tasks: taskReducer,
        user: userReducer, 
    },
});

export default store;
