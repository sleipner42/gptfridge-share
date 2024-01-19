import React, { useEffect, useState } from 'react';
import { Button, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import LoadingSpinner from './components/loading_bar';
import { baseUrl, port } from './config';

function Ingredients({ navigation, route }) {
    console.log('Ingredients')

    const [imageData, setImageData] = useState(null);
    const [data, setData] = useState(null);
    const [newItem, setNewItem] = useState('');

    const next = () => {
        navigation.navigate("Recipes", { data: data })
    };

    const handleAddItem = (newItem) => {
        const newList = [...data]
        newList.push(newItem)
        setData(newList);
    };

    const fetchData = async (formData) => {
        //console.log('imageData: ', formData);
        try {
            //const response = await fetch('http://localhost:8081/api/pti'); // Replace with your API URL
            console.log(`${baseUrl}:${port}/ingredients`);
            console.log(formData)
            const response = await fetch(`${baseUrl}:${port}/ingredients/image`, {
                method: 'POST',
                body: JSON.stringify(formData),
                headers: {
                    'Content-Type': 'application/json',
                },
            }); // Replace with your API URL
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const jsonData = await response.json();
            setData(jsonData.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    useEffect(() => {
        const images = route.params?.data;
        const sendData = []

        images.forEach((image, i) => {
            const fileObj = {
                image: image.base64,
                name: `image${i}.png`
            }
            sendData.push(fileObj);
        });
        setImageData(sendData)

    }, [route.params.data]);

    useEffect(() => {
        if (imageData) {
            fetchData(imageData);
        }
    }, [imageData]);



    const handleRemoveItem = (indexToRemove) => {
        const newDict = { ...data };
        // Remove the key from the copy
        //delete newDict[indexToRemove];
        newDict.ingredients.splice(indexToRemove, 1)

        setData(newDict);
    };

    return (
        <View style={styles.container}>
            <View style={styles.headerContainer}>
                <Text style={styles.headerText}>My ingredients</Text>
                <Text style={styles.countText}> • {data != null ? data.length : 0}</Text>
                <TouchableOpacity style={data == null ? styles.addButtonDisabled : styles.addButton}
                    disabled={data == null} onPress={() => {
                        navigation.navigate("AddIngredients", { addItem: handleAddItem })
                    }}>
                    <Text style={styles.addButtonText}>Add +</Text>
                </TouchableOpacity>
            </View>
            {data != null ?
                <View style={styles.ingredientContainer}>
                    {data.map((ingredient, index) => (
                        <View key={ingredient.name} style={styles.ingredientButton}>
                            <Text style={styles.ingredientText}>{ingredient.name}</Text>
                            <TouchableOpacity style={styles.deleteButton} onPress={() => handleRemoveItem(index)}>
                                <Icon name="close" size={18} style={styles.deleteText} />
                            </TouchableOpacity>
                        </View>
                    ))}
                </View>
                :
                <LoadingSpinner></LoadingSpinner>
            }
            <View style={styles.footer}>
                <View style={styles.buttonContainer}>
                    <Button
                        title="Next"
                        onPress={next}
                        disabled={data == null}
                    />
                </View>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        paddingHorizontal: 0,
        backgroundColor: '#F7F7F7',
        padding: 10,
        paddingLeft: 10,
        paddingRight: 10
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
        alignItems: 'center',  // vertically aligns items in the middle
        paddingVertical: 5,   // provides vertical padding
    },
    redCircle: {
        padding: 5,
        borderRadius: 5,
        marginTop: 5,
        backgroundColor: 'rgba(255, 69, 58, 1)',
        borderRadius: 20,
        width: 25,
        height: 25,
        justifyContent: 'center',
        alignItems: 'center',
        elevation: 5,
        borderWidth: 1,
        borderColor: "white"
    },
    whiteLine: {
        width: '80%',  // Set the width to 80% of the circle's width
        height: 2,  // Or any desired thickness for the line
        backgroundColor: 'white',
    },
    separator: {
        height: 1, // you can adjust the height
        width: '100%', // it should take the full width
        backgroundColor: '#E0E0E0', // a light grey color, you can adjust the color
        marginLeft: 0, // optional, to give the separator some left margin to be aligned with the text, adjust as needed
    },
    fab: {
        position: 'absolute',
        width: 56,
        height: 56,
        alignItems: 'center',
        justifyContent: 'center',
        right: 10,
        bottom: 10,
        backgroundColor: '#03A9F4',
        borderRadius: 28,
        elevation: 8,
    },
    fabIcon: {
        fontSize: 24,
        color: 'white',
    },
    headerContainer: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    headerText: {
        fontSize: 24,
        fontWeight: 'bold',
    },
    countText: {
        fontSize: 24,
    },
    addButton: {
        marginLeft: 'auto',
        backgroundColor: 'rgb(10,132,255)',
        padding: 10,
        borderRadius: 10,
    },
    addButtonDisabled: {
        marginLeft: 'auto',
        backgroundColor: 'rgba(10,132,255, 0.5)',
        padding: 10,
        borderRadius: 10,
    },
    addButtonText: {
        color: 'white',
        fontSize: 16,
    },
    ingredientContainer: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        justifyContent: 'start',
        marginTop: 15,
    },
    ingredientButton: {
        backgroundColor: 'rgb(255,255,255)',
        padding: 10,
        borderRadius: 20,
        margin: 5,
        shadowColor: "#000",
        shadowOffset: {
            width: 0,
            height: 0,
        },
        shadowOpacity: 0.05,
        shadowRadius: 10,
        flexDirection: 'row'
    },
    ingredientText: {
        color: 'black',
        fontSize: 16,
    },
    footer: {
        width: '100%',
        padding: 10,
        position: "absolute",
        bottom: 0,
    },
    deleteButton: {
        backgroundColor: 'rgba(255, 255, 255, 255)',
        borderRadius: 20,
        width: 20,
        height: 20,
        marginLeft: 5,
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 1.5,
        borderColor: "rgb(152,152,157)"
    },
    deleteText: {
        color: "rgb(152,152,157)",
        position: "absolute"
    },
});

export default Ingredients;
