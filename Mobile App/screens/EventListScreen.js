import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, ActivityIndicator, StyleSheet } from 'react-native';
import api from '../api';

export default function EventListScreen() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/events/')
      .then(response => setEvents(response.data))
      .catch(error => console.error(error))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <ActivityIndicator style={{ flex: 1 }} />;

  return (
    <View style={styles.container}>
      <FlatList
        data={events}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.eventItem}>
            <Text style={styles.title}>{item.title}</Text>
            <Text>{item.date}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  eventItem: { marginBottom: 16, padding: 16, backgroundColor: '#f0f0f0', borderRadius: 8 },
  title: { fontSize: 18, fontWeight: 'bold' },
});
