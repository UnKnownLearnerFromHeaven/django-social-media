from django.db import models
from django.contrib.auth.models import User 
from django.urls import reverse 



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    title = models.CharField(max_length=20)
    current_price = models.DecimalField(decimal_places=2, max_digits=8, default='0.00')
    starting_bid = models.DecimalField(decimal_places=2, max_digits=8, default='0.00')
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="Post_categories")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ('-title',)
    
    def __str__(self):
        return f"{self.title}"
    
    def like_count(self):
        return self.post_liked.count()
    
    def user_can_like(self, user):
        user_like = user.liker.filter(post=self)
        if user_like.exists():
            return False
        return True
    
    def get_absolute_url(self):
        return reverse("shop:detail", args=(self.id,))
    
    
class Bids(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, related_name='posts_bid')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    amount = models.DecimalField(decimal_places=2, max_digits=8, default=None)
    
    def __str__(self):
        return f"{self.user} bids on {self.post}, {self.amount}$"
    
    
class Category(models.Model):
    subject = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.subject}"
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_liked')
    
    def __str__(self):
        return f"{self.user} liked {self.post}"
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} commented on {self.post}"
    