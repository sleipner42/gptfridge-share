import React from 'react';
import { ActivityIndicator, StyleSheet, View, Text } from 'react-native';

const LoadingSpinner = () => (
    <View style={[styles.container]}>
        <View style={styles.spinnerContainer}>
            <ActivityIndicator size="large" />
            <Text>Loading...</Text>
        </View>
    </View>
);

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
    },
    spinnerContainer: {
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
        backgroundColor: 'rgba(0,0,0,0.1)',
        borderRadius: 10,
      },
});

export default LoadingSpinner;