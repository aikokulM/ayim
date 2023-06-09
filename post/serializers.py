from rest_framework import serializers
from django.db.models import Avg

from .models import Category, Post, PostImages


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerialiser(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source ='author.name')

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        author = Post.objects.create(author=user, **validated_data)
        return author

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes_count'] = instance.likes.count()
        representation['comments'] = [i.body for i in instance.comments.all()]
        representation['rating'] = instance.ratings.aggregate(Avg('rating'))
        ['rating_avg']

        return representation
    

class PostImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = 'all'

    def get_image_url(self,obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self.get_image_url(instance)
        return representation