import React, { useEffect, useState } from "react";
import {
    Dimensions,
    FlatList,
    Image,
    Linking,
    StyleSheet,
    Text,
    TouchableOpacity,
    View
} from "react-native";
import { baseUrl, port } from "./config";
//import RecipeData from './data';

function Recipes({ route }) {
    const data_from_ingredients = route.params?.data;
    console.log("Rollover data: ", data_from_ingredients);
    const [data, setData] = useState(null);

    const openURL = (url) => {
        Linking.canOpenURL(url).then((supported) => {
            if (supported) {
                Linking.openURL(url);
            } else {
                console.log("Don't know how to open URL: " + url);
            }
        });
    };

    const fetchData = async () => {
        try {

            const body = JSON.stringify(data_from_ingredients.map((obj) => obj.primary_key))
            console.log(body)
            const response = await fetch(`${baseUrl}:${port}/recipes/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: body,
            }); // Replace with your API URL
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            const jsonData = await response.json();
            setData(jsonData.data);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <View style={styles.container}>
            {data != null ? (
                <FlatList
                    style={styles.flatView}
                    data={data}
                    renderItem={({ item, index }) => (
                        <TouchableOpacity
                            onPress={() => openURL(item.recipe.url)}
                        >
                            <View style={styles.imageContainer}>
                                <Image
                                    style={styles.image}
                                    source={{ uri: item.recipe.image_url }}
                                />
                                <View style={styles.labelContainer}>
                                    <Text style={styles.label}>
                                        {item.recipe.name +
                                            " - " +
                                            item.match +
                                            "/" +
                                            item.recipe.nr_of_ingredients}
                                    </Text>
                                </View>
                            </View>
                        </TouchableOpacity>
                    )}
                    keyExtractor={(item, index) => index.toString()}
                    numColumns={2}
                />
            ) : (
                <Text>Loading data...</Text>
            )}
        </View>
    );
}

const { width } = Dimensions.get("window");
const itemWidth = width / 2;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 0,
    },
    flatView: {
        backgroundColor: "white",
        borderRadius: 10,
        minHeight: itemWidth * 2,
    },
    imageContainer: {
        width: itemWidth,
        height: itemWidth,
        padding: 10,
        position: "relative",
    },
    image: {
        flex: 1,
        width: null,
        height: null,
        resizeMode: "cover",
        borderRadius: 10,
    },
    labelContainer: {
        position: "absolute",
        bottom: 5,
        backgroundColor: "white",
        paddingHorizontal: 10,
        paddingVertical: 5,
        borderRadius: 5,
    },
    label: {
        fontSize: 16,
        fontWeight: "bold",
        color: "black",
    },
});

export default Recipes;
