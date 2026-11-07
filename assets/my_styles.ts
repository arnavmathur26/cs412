import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  scrollContainer: {
    paddingHorizontal: 20,
    paddingTop: 60,
    paddingBottom: 40,
  },
  titleText: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 12,
  },
  bodyText: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 16,
    lineHeight: 22,
  },
  sectionText: {
    fontSize: 16,
    marginTop: 16,
    marginBottom: 16,
    lineHeight: 22,
  },
  headlineText: {
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 20,
    marginBottom: 6,
  },
  bylineText: {
    fontSize: 13,
    color: '#666',
    marginBottom: 8,
  },
  image: {
    width: 250,
    height: 250,
    borderRadius: 8,
    marginVertical: 12,
  },
  wideImage: {
    width: '100%',
    height: 220,
    borderRadius: 8,
    marginVertical: 12,
  },
});
