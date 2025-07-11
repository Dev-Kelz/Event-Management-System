import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, Button } from 'react-native';

const EventListScreen = ({ navigation }) => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetch('http://192.168.1.10:8000/events/')
      .then(res => res.json())
      .then(data => setEvents(data))
      .catch(() => setEvents([]));
  }, []);

  return (
    <View>
      <Button title="Create Event" onPress={() => navigation.navigate('CreateEvent')} />
      <FlatList
        data={events}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => (
          <View style={{ padding: 10 }}>
            <Text style={{ fontWeight: 'bold' }}>{item.title}</Text>
            <Text>{item.date}</Text>
          </View>
        )}
      />
    </View>
  );
};

export default EventListScreen;