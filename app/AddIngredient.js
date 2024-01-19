import React, { useEffect, useState } from 'react';
import { FlatList, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import { baseUrl, port } from './config';

function AddIngredients({ route, navigation }) {

    const [searchResults, updateSearchResults] = useState([]);
    const [searchTerm, setSearchText] = useState('');
    const [allIngredients, setAllIngredients] = useState([])

    const { addItem } = route.params;

    const AddIngredient = (item) => {
        addItem(item)
        navigation.goBack()
    };

    const fetchData = async () => {
        try {

            const response = await fetch(`${baseUrl}:${port}/ingredients/`, {
                method: "GET"
            }); // Replace with your API URL
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            const jsonData = await response.json();
            setAllIngredients(jsonData.data);
            updateSearchResults(jsonData.data)
            console.log(searchResults)

        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const autoComplete = (searchTerm) => {
        setSearchText(searchTerm)

        const normalizedTerm = searchTerm.toLowerCase().trim();
        const filteredIngredients = allIngredients.filter(item => {
            return Object.values(item).some(value =>
                String(value).toLowerCase().includes(normalizedTerm)
            );
        });

        updateSearchResults(filteredIngredients)
    }

    return (
        <View style={styles.container}>

            <View style={styles.rowContainer}>
                <TextInput
                    value={searchTerm}
                    onChangeText={autoComplete}
                    placeholder="Type to search ingredient"
                    style={styles.item}
                    autoFocus={true}
                />
            </View>
            <FlatList
                style={styles.flatList}
                data={searchResults}
                renderItem={({ item, index }) => (
                    <View style={styles.rowContainer}>
                        <Text key={index} style={styles.item}>{item.name}</Text>
                        <TouchableOpacity
                            style={styles.fab}
                            onPress={() => {
                                AddIngredient(item)
                            }}
                        >
                            <Text style={styles.fabIcon}>+</Text>
                        </TouchableOpacity>
                    </View>
                )}
                keyExtractor={(item, index) => index.toString()}
                ItemSeparatorComponent={() => <View style={styles.separator} />}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        paddingHorizontal: 0,
        backgroundColor: '#F7F7F7',
    },
    flatList: {
        paddingHorizontal: 10,
    },
    item: {
        fontSize: 20,
        padding: 10,
        borderBottomColor: '#ccc',
        borderBottomWidth: 0,
    },
    inputContainer: {
        padding: 10,
        backgroundColor: '#eee',  // Optional: for visual separation
    },
    input: {
        height: 40,
        borderColor: 'gray',
        borderWidth: 1,
        paddingLeft: 10,
    },
    footer: {
        //position: 'absolute',
        left: 0,
        right: 0,
        bottom: 0,
        height: 80,
        backgroundColor: '#eee',
        justifyContent: 'center',
        alignItems: 'center',
        padding: 10,
    },
    listItemContainer: {
        flex: 1,
        margin: 5,
    },
    rowContainer: {
        flexDirection: 'row', // places items horizontally
        justifyContent: 'space-between',
        alignItems: 'center',  // vertically aligns items in the middle
        paddingVertical: 5,   // provides vertical padding
    },
    fab: {
        width: 30,
        height: 30,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'rgb(52,199,89)',
        borderRadius: 28,
        elevation: 8,
    },
    fabIcon: {
        fontSize: 24,
        color: 'white',
    },
    separator: {
        height: 1, // you can adjust the height
        width: '100%', // it should take the full width
        backgroundColor: '#E0E0E0', // a light grey color, you can adjust the color
        marginLeft: 0, // optional, to give the separator some left margin to be aligned with the text, adjust as needed
    },
});

export default AddIngredients;
