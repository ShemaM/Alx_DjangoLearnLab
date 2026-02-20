from rest_framework import serializers

from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'author_username',
            'title',
            'content',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'author', 'author_username', 'created_at', 'updated_at')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = (
            'id',
            'post',
            'author',
            'author_username',
            'content',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'author', 'author_username', 'created_at', 'updated_at')

