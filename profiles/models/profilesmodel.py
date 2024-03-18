from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
class category(models.Model):
    code = models.CharField(max_length=32,null=True, blank=True)
    name = models.CharField(max_length=128,unique=True)
class subcategory(models.Model):
    code = models.CharField(max_length=32,null=True, blank=True)
    name = models.CharField(max_length=128,unique=True)
    category = models.ForeignKey(category, on_delete=models.SET_NULL, null=True)
class PostModel(models.Model):
    title = models.CharField(max_length=100,null=True, blank=True)
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class CommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE,related_name='commentmodel_set')
    comment = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)

