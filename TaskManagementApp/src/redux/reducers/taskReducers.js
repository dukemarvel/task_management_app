import { ADD_TASK, REMOVE_TASK, UPDATE_TASK, SET_TASKS, SET_TASK, DELETE_TASK } from '../actions/taskActions';

const initialState = {
    tasks: [],
    currentTask: null,
};

const taskReducer = (state = initialState, action) => {
    switch (action.type) {
        case 'SET_TASKS':  
            console.log('Reducer SET_TASKS:', action.payload);  
            return {
                ...state,
                tasks: action.payload, 
            };
        case SET_TASK:
            return {
                ...state,
                currentTask: action.payload,
            };
        case ADD_TASK:
            return {
                ...state,
                tasks: [...state.tasks, action.payload],
            };
        case REMOVE_TASK:
        case DELETE_TASK:
            return {
                ...state,
                tasks: state.tasks.filter(task => task.id !== action.payload),
            };
        case UPDATE_TASK:
            return {
                ...state,
                tasks: state.tasks.map(task => 
                    task.id === action.payload.id ? action.payload : task
                ),
            };
        default:
            return state;
    }
};

export default taskReducer;
