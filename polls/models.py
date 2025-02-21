from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    
class Question(models.Model):
    question_text = models.CharField(max_length=255)
    published_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    allow_multiple_choice = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    def has_expired(self):
        return self.expiry_date and timezone.now() > self.expiry_date
    
    def __str__(self):
        return self.question_text
    

class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text
    

class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE, 
                             null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    voted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user','choice') # Prevent duplicate votes per user
    
    
class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return F"{self.user.username}:{self.text[:30]}..."