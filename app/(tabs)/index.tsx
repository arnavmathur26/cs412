import { Image, Text, View } from 'react-native';

import { styles } from '../../assets/my_styles';

export default function IndexScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.titleText}>Welcome to NBA News</Text>
      <Text style={styles.bodyText}>
        Not a day goes by without something new and exciting happening in the basketball world, and 
        with my app, you can stay on top of all of it! Catch up on major headlines, close games, 
        crazy performances, and more! 
      </Text>
        <Image
        source={require('../../assets/images/nba-news-logo.png')}
        style={{ width: 180, height: 180, resizeMode: 'contain', marginBottom: 12 }}
      />
    </View>
  );
}
