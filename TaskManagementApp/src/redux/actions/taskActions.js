import { 
    getTasks as fetchTasksFromApi, 
    getTask as fetchTaskFromApi, 
    createTask as createTaskApi, 
    updateTask as updateTaskApi, 
    deleteTask as deleteTaskApi 
} from '../../api/taskApi'; 


export const fetchTasks = () => {
    return async (dispatch) => {
        try {
            const tasks = await fetchTasksFromApi();
            console.log('Fetched tasks, Action Level:', tasks); 
            dispatch({
                type: 'SET_TASKS',
                payload: tasks,
            });
        } catch (error) {
            console.error('Error fetching tasks', error);
        }
    };
};


export const fetchTask = (taskId) => {
    return async (dispatch) => {
        try {
            const task = await fetchTaskFromApi(taskId);
            dispatch({
                type: 'SET_TASK',
                payload: task,
            });
        } catch (error) {
            console.error('Error fetching task', error);
        }
    };
};

export const addTask = (task) => {
    return async (dispatch) => {
        try {
            const newTask = await createTaskApi(task);
            dispatch({
                type: 'ADD_TASK',
                payload: newTask, 
            });
        } catch (error) {
            console.error('Error adding task', error);
        }
    };
};



export const updateTask = (taskId, task) => {
    return async (dispatch) => {
        try {
            const updatedTask = await updateTaskApi(taskId, task);
            dispatch({
                type: 'UPDATE_TASK',
                payload: updatedTask,
            });
        } catch (error) {
            console.error('Error updating task', error);
        }
    };
};


export const deleteTask = (taskId) => {
    return async (dispatch) => {
        try {
            await deleteTaskApi(taskId);
            dispatch({
                type: 'DELETE_TASK',
                payload: taskId,
            });
        } catch (error) {
            console.error('Error deleting task', error);
        }
    };
};

// Action to remove a task from the store (typically used when syncing state with the server)
export const removeTask = (taskId) => ({
    type: 'REMOVE_TASK',
    payload: taskId,
});
