import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { addTask, updateTask } from '../redux/actions/taskActions';
import { useNavigation } from '@react-navigation/native';

const TaskFormScreen = ({ route }) => {
    const navigation = useNavigation();
    const { taskId } = route.params || {};
    const dispatch = useDispatch();
    const task = useSelector(state => 
        taskId ? state.tasks.tasks.find(t => t.id === taskId) : null
    );

    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [status, setStatus] = useState('');
    const [dueDate, setDueDate] = useState('');


    useEffect(() => {
        if (task) {
            setTitle(task.title);
            setDescription(task.description);
            setStatus(task.status);
            setDueDate(task.due_date);
        }
    }, [task]);

    const handleSave = () => {
        if (!title || !description) {
            Alert.alert('Validation Error', 'Title and description are required.');
            return;
        }

        if (task) {
            
            dispatch(updateTask(task.id, { 
                title, 
                description, 
                status, 
                due_date: dueDate, 
                owner_id: task.owner_id 
            }));
        } else {
            
            dispatch(addTask({
                title,
                description,
                status,
                due_date: dueDate,
                owner_id: 1  
            }));
        }
        navigation.goBack(); 
    };

    return (
        <View style={{ padding: 16 }}>
            <Text>Task Title</Text>
            <TextInput 
                value={title} 
                onChangeText={setTitle} 
                placeholder="Enter task title"
                style={{ borderBottomWidth: 1, marginBottom: 12 }} 
            />

            <Text>Task Description</Text>
            <TextInput 
                value={description} 
                onChangeText={setDescription} 
                placeholder="Enter task description"
                style={{ borderBottomWidth: 1, marginBottom: 12 }} 
            />

            <Text>Task Status</Text>
            <TextInput 
                value={status} 
                onChangeText={setStatus} 
                placeholder="Enter task status"
                style={{ borderBottomWidth: 1, marginBottom: 12 }} 
            />

            <Text>Due Date</Text>
            <TextInput 
                value={dueDate} 
                onChangeText={setDueDate} 
                placeholder="YYYY-MM-DD" 
                style={{ borderBottomWidth: 1, marginBottom: 12 }} 
            />

            <Button title="Save Task" onPress={handleSave} />
        </View>
    );
};

export default TaskFormScreen;
