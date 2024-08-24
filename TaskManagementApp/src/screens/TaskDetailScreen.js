import React, { useState } from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { addTask, updateTask } from '../redux/actions';

const TaskDetailScreen = ({ route, navigation }) => {
    const { taskId } = route.params || {};
    const dispatch = useDispatch();
    const task = useSelector(state => state.tasks.tasks.find(t => t.id === taskId));
    const [title, setTitle] = useState(task ? task.title : '');

    const handleSave = () => {
        if (task) {
            dispatch(updateTask({ ...task, title }));
        } else {
            dispatch(addTask({ id: Date.now().toString(), title }));
        }
        navigation.goBack();
    };

    return (
        <View>
            <Text>Task Title</Text>
            <TextInput value={title} onChangeText={setTitle} />
            <Button title="Save" onPress={handleSave} />
        </View>
    );
};

export default TaskDetailScreen;
