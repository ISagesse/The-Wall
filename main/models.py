from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):
    def user_validator(self, post_data):
        errors = {}

        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(post_data['first_name']) < 3:
            errors['first_name'] = 'The first name must be more than 3 character'

        if len(post_data['last_name']) < 3:
            errors['last_name'] = 'The last name must be more than 3 character'

        if not email_checker.match(post_data['email']):
            errors['email'] = 'Invalid email address!'

        if post_data['password'] != post_data['cf_password']:
            errors['password'] = 'passwords do not match '

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=95)
    last_name = models.CharField(max_length=95)
    email = models.CharField(max_length=225)
    password = models.CharField(max_length=395)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)