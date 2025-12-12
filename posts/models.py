from django.db import models

"""
create table post (
id int autoicrement primary key
name varchar(255) not null,
content varchar(1000)
)
"""
"""insert into post titlle, content VALUES(title1, content1) ==> Post.objects.create(title="title1", content="content1")
"""


class Category(models.Model):
 name = models.CharField(max_length=255)
 def __str__(self):
    return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=156)

    def __str__(self):
        return self.name
   


# title, content, rate, created_at, updated_at
class Post(models.Model):
    image = models.ImageField(null=True, blank=True)    
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=1000, null=True, blank=True)
    rate = models.IntegerField(default=0, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    tag = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.content}"
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.author}"