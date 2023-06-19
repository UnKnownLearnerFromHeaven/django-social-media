from django import forms 
from django.contrib.auth.models import User
from .models import Post, Bids, Comment


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'category')
        

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'category', 'starting_bid')
        
        
class BidForm(forms.ModelForm):
    class Meta:
        model = Bids 
        fields = ('amount',)
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        
class AddCommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {
            'body': 'your reply'
        }
        
class SearchForm(forms.Form):
    search = forms.CharField(label='search')
    