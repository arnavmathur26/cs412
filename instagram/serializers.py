from rest_framework import serializers

from .models import Photo, Posts, Profile

class ProfileSerializer(serializers.ModelSerializer):
    num_followers = serializers.SerializerMethodField()
    num_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'username', 'display_name', 'profile_image_url', 'bio_text', 'join_date', 'user',
                   'num_followers', 'num_following']

    def get_num_followers(self, obj):
        return obj.get_num_followers()

    def get_num_following(self, obj):
        return obj.get_num_following()
    
class PhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'image_url', 'timestamp']

    def get_image_url(self, obj):
        request = self.context.get('request')
        url = obj.get_image_url()
        if request is not None:
            return request.build_absolute_uri(url)
        return url

class PostsSerializer(serializers.ModelSerializer):
    num_comments = serializers.SerializerMethodField()
    num_likes = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    profile_id = serializers.IntegerField(source='profile.id', read_only=True)
    profile_username = serializers.CharField(source='profile.username', read_only=True)
    profile_display_name = serializers.CharField(source='profile.display_name', read_only=True)

    class Meta:
        model = Posts
        fields = ['id', 'caption', 'timestamp', 'num_comments', 'num_likes', 'photos',
                  'profile_id', 'profile_username', 'profile_display_name']

    def get_num_comments(self, obj):
        return obj.get_num_comments()

    def get_num_likes(self, obj):
        return obj.get_num_likes()

    def get_photos(self, obj):
        return PhotoSerializer(obj.get_photos(), many=True, context=self.context).data

