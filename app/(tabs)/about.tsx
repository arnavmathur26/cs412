import { Image, Text, View } from 'react-native';

import { styles } from '../../assets/my_styles';

export default function AboutScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.titleText}>About This App</Text>
      <Text style={styles.bodyText}>
        Welcome to the NBA News app! Here you can get caught up on everything basketball, all in one place!
      </Text>
      <Image
        source={require('../../assets/images/nba-news-logo.png')}
        style={{ width: 180, height: 180, resizeMode: 'contain', marginBottom: 12 }}
      />
    </View>
  );
}
