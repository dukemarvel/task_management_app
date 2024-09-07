import React, { useEffect } from 'react';
import { View, Text, Button, FlatList } from 'react-native';
import { useSelector, useDispatch } from 'react-redux';
import { fetchTasks, deleteTask } from '../redux/actions/taskActions';

const TaskListScreen = ({ navigation }) => {
    const tasks = useSelector(state => state.tasks.tasks);
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(fetchTasks());
    }, [dispatch]);

    

    const renderItem = ({ item }) => (
        <View>
            <Text>{item.title}</Text>
            <Button title="View Details" onPress={() => navigation.navigate('TaskForm', { taskId: item.id })} />

            
            <Button title="Remove Task" onPress={() => dispatch(deleteTask(item.id))} />
        </View>
    );

    return (
        <View>
            <FlatList
                data={tasks}
                renderItem={renderItem}
                keyExtractor={item => item.id.toString()}
            />
            <Button title="Add Task" onPress={() => navigation.navigate('TaskForm')} />
        </View>
    );
};

export default TaskListScreen;
