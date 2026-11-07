import { Image, ScrollView, Text } from 'react-native';

import { styles } from '../../assets/my_styles';

export default function DetailScreen() {
  return (
    <ScrollView contentContainerStyle={styles.scrollContainer}>
      <Text style={styles.titleText}>NBA Headlines</Text>

      <Text style={styles.headlineText}>
        Tatum Wins it in Overtime
      </Text>
      <Text style={styles.bylineText}>NBA Wire - Celtics v Nets</Text>
      <Text style={styles.sectionText}>
        In a close game last tuesday, Jayson Tatum hit the game winning shot for the Celtics to beat the Nets in overtime
         125-124. Tatum ended the night with a wopping 40 points and 8 assists. His game winner capped off an incredible 
         performance, and further proved the doubters of the Jaylen Brown trade wrong. Tatum and the Celtics are cementing themselves 
         as true contenders to win it all this year!
      </Text>

      <Image
        source={require('../../assets/images/tatum.jpg')}
        style={styles.wideImage}
      />

      <Text style={styles.headlineText}>
        Rookie Sensation Turning Heads Early in the Season
      </Text>
      <Text style={styles.bylineText}>NBA Wire - Caleb Wilson</Text>
      <Text style={styles.sectionText}>
        Caleb Wilson has been putting on a show for the Chicago Bulls in his first few games in the NBA. The exciting young forward 
        is averaging 19.5 points per game, and could be Chicago's final piece to reclaiming playoff success. Caleb's athleticism, and
        offensive freedom has made him one of the most exciting young talents in the league.
      </Text>

      <Image
        source={require('../../assets/images/caleb.jpeg')}
        style={styles.wideImage}
      />

      <Text style={styles.headlineText}>
        Giannis lead Heat face early-season woes
      </Text>
      <Text style={styles.bylineText}>NBA Wire - Miami Heat</Text>
      <Text style={styles.sectionText}>
        Giannis Antetokounmpo made the shocking move to South Beach last summer. After some highs and lows in Milwalke,
        including an NBA championship in 2021, Giannis decided it was high-time for a change of scenery, as the Bucks front
        office struggled to build a contending team around the Greek superstar. Yet the Heat have started the 2026 season 3-6,
        with few positives to takeaway. Many argued that a trade would only leave Giannis in the same position as before,
        the players and draft capital the heat gave up to aquire Giannis now leave the team with little depth, and no offensive
        threat outside of the Greek Freak.
      </Text>

      <Image
        source={require('../../assets/images/giannis.jpg')}
        style={[styles.wideImage, { height: 400 }]}
      />
      </ScrollView>
  );
}
