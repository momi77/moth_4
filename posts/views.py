from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from random import randint
from posts.models import Post, Comment
from .forms import PostCreateForm, CommentForm, SearchForm
from django.contrib.auth.decorators import login_required 
from django.db.models import Q  
from posts.forms import PostUpdateForm


"""
posts = [post1, post2, post3, post4, post5, post6, post7, post8, post9, post10, post11, post12, post13, post14, post15, post16]
limit = 5
page = 3
start = (page - 1) * limit
end = page * limit
"""


def test_view(request):
    return HttpResponse(f"This is a test view.{randint(1,1000)}")



def html_view(request):
    if request.method == "GET":
        return render(request,"base.html")
    
@login_required(login_url='/login/')
def list_view(request):
    posts = Post.objects.all()
    form = SearchForm()
    limit = 5
    if request.method == "GET":
        print(request.GET)
        search = request.GET.get('search')
        category_id = request.GET.get('category')
        tags_ids = request.GET.get('tags_ids')
        ordering = request.GET.get('ordering')
        page = int(request.GET.get('page')) if request.GET.get('page') else 1
        if search:
            posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))
        if category_id:
            posts = posts.filter(category__id=category_id)
        if tags_ids:
            posts = posts.filter(tag__id__in=tags_ids)
        if ordering and ordering!= "None":
            posts = posts.order_by(ordering)   
            
        post_count = posts.count()
        insufficient = post_count % limit 
        max_pages = post_count / limit if insufficient < 1 else post_count / limit + 1
        start = (page - 1) * limit
        end = page * limit
        posts = posts[start:end]    

        return render(request, "post/list_view.html", context={"posts": posts, "form": form, "max_pages": range(1, int(max_pages+1))})

@login_required(login_url='/login/')
def post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
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
    

def post_update_view(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    if not post:
        return redirect("/profile/")
    if request.method == "GET":
        form = PostUpdateForm(instance=post)
        return render(request, "list_view/post_update.html", context={"form": form})
    if request.method == "POST":
        form = PostUpdateForm(request.POST, request.FILES, instance=post)
        if not form.is_valid():
            return render(request, "list_view/post_update.html", context={"form": form})
        form.save()
        return redirect(f"/profile/")