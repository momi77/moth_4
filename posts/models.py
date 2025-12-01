from django.db import models

"""
create table post (
id int autoicrement primary key
name varchar(255) not null,
content varchar(1000)
)
"""


# title, content, rate, created_at, updated_at
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=1000, null=True, blank=True)
    rate = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.content}"