from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator
from django.db import models

POST_MAX_LENGTH = 280


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=POST_MAX_LENGTH, validators=[MaxLengthValidator(
        POST_MAX_LENGTH, "Must be less than 280 characters.")])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content} (id:{self.id}) by {self.author}"

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "content": self.content,
            "timestamp": self.timestamp,
            "num_likes": self.liked_users.all().count()
        }


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="liked_users")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="liked_posts")

    def __str__(self):
        return f"post id {self.post.id} by {self.post.author} liked by {self.user}"


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f"{self.follower} following {self.user}"
