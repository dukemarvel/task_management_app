import api from './api';

export const getTask = async (taskId) => {
    try {
        const response = await api.get(`/tasks/${taskId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching task', error);
    }
};

export const getTasks = async () => {
    try {
        const response = await api.get('/tasks');
        return response.data;
    } catch (error) {
        console.error('Error fetching tasks', error);
    }
};

export const createTask = async (task) => {
    try {
        const response = await api.post(
            '/tasks',
            task,
            {
                headers: {
                    'Content-Type': 'application/json',
                },
            }
        );
        return response.data;
    } catch (error) {
        console.error('Error creating task', error);
    }
};

export const updateTask = async (taskId, task) => {
    try {

        console.log("task to be updated: taskid: ", taskId)
        console.log("task object: ", task)
        const response = await api.put(
            `/tasks/${taskId}`,
            task,
            {
                headers: {
                    'Content-Type': 'application/json',
                },
            }
        );
        return response.data;
    } catch (error) {
        console.error('Error updating task', error);
    }
};

export const deleteTask = async (taskId) => {
    try {
        const response = await api.delete(`/tasks/${taskId}`);
        return response.data;
    } catch (error) {
        console.error('Error deleting task', error);
    }
};
