from rest_framework import serializers
from profiles.models.profilesmodel import Profile,category,subcategory,PostModel, CommentModel
# #ECF_AP_Debit
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields=['id', 'name', 'email', 'profile_picture']
class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = subcategory
        fields = ['id','code', 'name']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True,source='subcategory_set')

    class Meta:
        model = category
        fields = ['id','code', 'name', 'subcategories']
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['comment', 'publication_date']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, source='commentmodel_set')
    total_comments = serializers.SerializerMethodField()

    def get_total_comments(self, obj):
        return obj.commentmodel_set.count()

    class Meta:
        model = PostModel
        fields = ['id', 'title', 'author', 'created_at', 'comments', 'total_comments']
