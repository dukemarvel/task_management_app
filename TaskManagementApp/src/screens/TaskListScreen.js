import React from 'react';
import { View, Text, Button, FlatList } from 'react-native';
import { useSelector, useDispatch } from 'react-redux';
import { removeTask } from '../redux/actions';

const TaskListScreen = ({ navigation }) => {
    const tasks = useSelector(state => state.tasks.tasks);
    const dispatch = useDispatch();

    const renderItem = ({ item }) => (
        <View>
            <Text>{item.title}</Text>
            <Button title="View Details" onPress={() => navigation.navigate('TaskDetail', { taskId: item.id })} />
            <Button title="Remove Task" onPress={() => dispatch(removeTask(item.id))} />
        </View>
    );

    return (
        <View>
            <FlatList
                data={tasks}
                renderItem={renderItem}
                keyExtractor={item => item.id}
            />
            <Button title="Add Task" onPress={() => navigation.navigate('TaskDetail')} />
        </View>
    );
};

export default TaskListScreen;
