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
    
class PostsSerializer(serializers.ModelSerializer):
    num_comments = serializers.SerializerMethodField()
    num_likes = serializers.SerializerMethodField()

    class Meta:
        model = Posts
        fields = ['id', 'image_url', 'image_file', 'timestamp', 'num_comments', 'num_likes']

    def get_num_comments(self, obj):
        return obj.get_num_comments()
    
    def get_num_likes(self, obj):
        return obj.get_num_likes()
    
