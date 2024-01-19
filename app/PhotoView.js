import { React, useState } from 'react';
import { SafeAreaView, StyleSheet, View, Button, FlatList, Image, Dimensions, TouchableOpacity, Text } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

const PhotoView = ({ navigation }) => {

    const [status, requestPermission] = ImagePicker.useCameraPermissions();
    requestPermission()
    const [images, setImages] = useState([]);

    const handleDelete = (index) => {
        setImages(prevImages => {
            let newImages = [...prevImages];
            newImages.splice(index, 1);
            return newImages;
        });
    };

    const pickImage = async () => {
        let result = await ImagePicker.launchCameraAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.All,
            quality: 0,
            base64: true
        });

        if (result.assets) {
            setImages(prevImages => {
                let newImages = [...prevImages];
                newImages.push(result.assets[0]);
                return newImages;
            });
        }
    };

    const next = () => {
        console.log('Going to Your ingredients')
        navigation.navigate("Your ingredients", { data: images })
    };

    const handleItemClick = (index) => {
        if (index === images.length - 1) {  // If the tapped image is the last item
            console.log("hello world");
            pickImage()
        }
    };


    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.textView}>
                <Icon name="fridge" size={50} />
                <Text style={{ fontSize: 20, margin: 10 }}>What's in your fridge?</Text>
                <Text style={{ fontSize: 14 }}>Take some photos on the <Text style={{ fontWeight: "bold" }}>ingredients</Text> in your <Text style={{ fontWeight: "bold" }}>fridge</Text>.</Text>
            </View>
            <View style={styles.flatViewContainer}>
                <FlatList
                    style={styles.flatView}
                    data={images}
                    renderItem={({ item, index }) => (
                        <View style={styles.imageContainer}>
                            <Image style={styles.image} source={{ uri: item.uri }} onTouchEnd={() => handleItemClick(index)} />
                            <TouchableOpacity style={styles.deleteButton} onPress={() => handleDelete(index)}>
                                <Text style={styles.deleteText}>X</Text>
                            </TouchableOpacity>
                        </View>
                    )}
                    keyExtractor={(item, index) => index.toString()}
                    numColumns={3}
                />
            </View>

            <Button
                title="+ Add photo"
                onPress={pickImage}
            />
            <View style={styles.footer}>
                <View style={styles.buttonContainer}>
                    <Button
                        title="Next"
                        onPress={next}
                    />
                </View>
            </View>
        </SafeAreaView>
    );
};

const { width } = Dimensions.get('window');
const itemWidth = (width - 10 * 2) / 3;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 10,
        backgroundColor: 'rgba(242, 242, 247, 1)',
    },
    textView: {
        height: 170,
        justifyContent: 'center', // This centers children vertically in the view.
        alignItems: 'center'
    },
    flatViewContainer: {
        padding: 10,
    },
    flatView: {
        backgroundColor: "white",
        borderRadius: 10,
        minHeight: itemWidth * 2
    },
    imageContainer: {
        width: itemWidth,
        height: itemWidth,
        padding: 10,
        position: 'relative',
    },
    deleteButton: {
        position: 'absolute',
        top: 5,
        right: 5,
        backgroundColor: 'rgba(255, 69, 58, 1)',
        borderRadius: 20,
        width: 25,
        height: 25,
        justifyContent: 'center',
        alignItems: 'center',
        shadowColor: "#000",
        shadowOffset: {
            width: 0,
            height: 2,
        },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
        elevation: 5,
        borderWidth: 1,
        borderColor: "white"
    },
    deleteText: {
        fontWeight: 'bold',
        color: 'white',
    },
    image: {
        flex: 1,
        width: null,
        height: null,
        resizeMode: 'cover',
        borderRadius: 10,
    },
    footer: {
        width: '100%',
        padding: 10,
        position: "absolute",
        bottom: 30,
    }
});

export default PhotoView;
