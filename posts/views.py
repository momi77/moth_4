from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from random import randint
from posts.models import Post
from .forms import PostCreateForm, CommentForm
from django.contrib.auth.decorators import login_required    


def test_view(request):
    return HttpResponse(f"This is a test view.{randint(1,1000)}")



def html_view(request):
    if request.method == "GET":
        return render(request,"base.html")
    
@login_required(login_url='/login/')
def list_view(request):
    if request.method == "GET":
        posts = Post.objects.all()
        return render(request, "post/list_view.html", context={"posts": posts})
@login_required(login_url='/login/')    
# detail_view
def post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'post/detail_list_view.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })
@login_required(login_url='/login/')
def post_create_view(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/list_view/')
    else:
        form = PostCreateForm()
        return render(request, "post/post_create.html", context={"form": form})
    
    
