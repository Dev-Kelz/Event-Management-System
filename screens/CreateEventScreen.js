import React, { useState } from 'react';
import { View, TextInput, Button, Alert } from 'react-native';

const CreateEventScreen = ({ navigation }) => {
  const [title, setTitle] = useState('');
  const [date, setDate] = useState('');

  const handleCreate = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000//events/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id: Math.floor(Math.random() * 100000), // Simple random ID for demo
          title,
          date,
        }),
      });
      if (response.ok) {
        Alert.alert('Success', 'Event created!');
        navigation.goBack();
      } else {
        Alert.alert('Error', 'Could not create event.');
      }
    } catch {
      Alert.alert('Error', 'Server not reachable.');
    }
  };

  return (
    <View>
      <TextInput placeholder="Title" value={title} onChangeText={setTitle} />
      <TextInput placeholder="Date (YYYY-MM-DD)" value={date} onChangeText={setDate} />
      <Button title="Create" onPress={handleCreate} />
    </View>
  );
};

export default CreateEventScreen;