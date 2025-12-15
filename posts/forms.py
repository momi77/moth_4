from django import forms
from posts.models import Post, Comment, Category, Tag




class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']  
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    tags_ids = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    ordering = (
        ("None", "None"),
        ("created_at", "Created at"),
        ("-created_at", "Created at (desc)"),
        ("updated_at", "Updated at"),
        ("-updated_at", "Updated at (desc)"),
        ("rate", "Rate"),
        ("-rate", "Rate (desc)"),
        ("title", "Title"),
        ("-title", "Title (desc)"),
        ("?", "Random")
    )

    ordering = forms.ChoiceField(choices=ordering, required=False)