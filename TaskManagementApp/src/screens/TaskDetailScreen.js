import React, { useState } from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { addTask, updateTask } from '../redux/actions';
import { useNavigation } from '@react-navigation/native';

const TaskDetailScreen = ({ route }) => {
    const navigation = useNavigation();
    const { taskId } = route.params || {};
    const dispatch = useDispatch();
    const task = useSelector(state => state.tasks.tasks.find(t => t.id === taskId));

    const [title, setTitle] = useState(task ? task.title : '');
    const [description, setDescription] = useState(task ? task.description : '');
    const [status, setStatus] = useState(task ? task.status : '');
    const [dueDate, setDueDate] = useState(task ? task.due_date : '');

    const handleSave = () => {
        if (task) {
            dispatch(updateTask({ id: task.id, title, description, status, due_date: dueDate, owner_id: task.owner_id }));
        } else {
            dispatch(addTask({ title, description, status, due_date: dueDate, owner_id: 1 }));
        }
        navigation.goBack();  // Navigate back to the previous screen
    };

    return (
        <View>
            <Text>Task Title</Text>
            <TextInput value={title} onChangeText={setTitle} />

            <Text>Task Description</Text>
            <TextInput value={description} onChangeText={setDescription} />

            <Text>Task Status</Text>
            <TextInput value={status} onChangeText={setStatus} />

            <Text>Due Date</Text>
            <TextInput value={dueDate} onChangeText={setDueDate} placeholder="YYYY-MM-DD" />

            <Button title="Save Task" onPress={handleSave} />
        </View>
    );
};

export default TaskDetailScreen;
