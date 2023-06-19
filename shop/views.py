from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from .models import Post, Bids, Category, Like, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostEditForm, CreatePostForm, BidForm, CommentForm, AddCommentReplyForm, SearchForm
from django.contrib import messages
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomePageView(View):
    form_class = SearchForm
     
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(title__contains=request.GET['search'])
        return render(request, 'shop/home.html', {
            "posts": posts,
            "form": self.form_class
        })
        

class PostDetailView(View):
    form_class = CommentForm
    form_class_reply = AddCommentReplyForm
    
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        self.comments = self.post_instance.pcomments.filter(is_reply=False)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like = True
        return render(request, 'shop/detial.html', {
            "post": self.post_instance,
            "comments": self.comments,
            "form": self.form_class ,
            "reply_form": self.form_class_reply,
            "can_like": can_like,
        })
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, "Your comment submitted successfully", "success")
        return redirect('shop:detail', self.post_instance.id)
        
        
class PostEditView(LoginRequiredMixin, View):
    form_class = PostEditForm
    
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)
    
    
    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, "Just the owner can edit this post", "danger")
            return redirect("shop:home")
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.post_instance)
        return render(request, 'shop/edit_post.html', {
            "form": form 
        })
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.post_instance)
        if form.is_valid():
            form.save()
        return redirect("shop:detail", self.post_instance.id)
            
    
    
class CreatePostView(LoginRequiredMixin, View):
    form_class = CreatePostForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'shop/create_post.html', {
            "form": form
        })
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
        return redirect("shop:home")
    

class TakeBidView(LoginRequiredMixin, View):
    form_class = BidForm
    
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'shop/new_bid.html', {
            "form": form
        })
        
        
    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data['amount']
            if cd >= post.current_price:
                post.current_price = cd
                post.owner = request.user
                post.save()
        return redirect('shop:detail', post.id)
    
    
class PostLikeView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        like = Like.objects.filter(user=request.user, post=post)
        if like.exists():
            messages.error(request, 'you have already liked this post', 'danger')
        else:
            Like.objects.create(user=request.user, post=post)
            messages.success(request, 'You like this post', 'success')
        return redirect('shop:detail', post.id)
    
    
class PostDeleteView(LoginRequiredMixin, View):
    
    def get(self, request, post_id):
        post_instance = Post.objects.get(id=post_id)
        if request.user.id == post_instance.user.id :
            post_instance.delete()
            messages.success(request, 'You deleted this post successfully', 'success')
        else:
            messages.error(request, 'You can not delete this post', 'danger')
        return redirect('shop:home')


class AddReplyCommentView(LoginRequiredMixin, View):
    form_class = AddCommentReplyForm
    
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        comment = get_object_or_404(Comment, pk=kwargs['comment_id'])
        form = self.form_class(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.reply = comment
            new_reply.is_reply = True 
            new_reply.save()
            messages.success(request, 'Your comment submitted successfully', 'success')
        return redirect('shop:detail', post.id)