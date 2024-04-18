from django.db import models
  
class Word(models.Model):  
    word_id = models.AutoField(primary_key=True)  
    word_string = models.CharField(max_length=255)  
  
    def __str__(self):  
        return self.word_string
    
class News(models.Model):
    title = models.TextField(max_length=100)
    body = models.TextField(max_length=3000)
    url = models.TextField(max_length=500)
    time = models.TextField(max_length=30)
    keyword = models.TextField(max_length=100)
    pic = models.TextField(max_length=500)
    source = models.TextField(max_length=20)
    popularity = models.TextField(max_length=10)
    beginning = models.TextField(max_length=100)
    comment_cnt = models.IntegerField()

class Category(models.Model):
    name = models.TextField(max_length=20)
    news_cnt = models.TextField(max_length=20)
    news_list = models.TextField(max_length=2000)

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.TextField(max_length=10)
    content = models.TextField(max_length=100)
    time = models.TextField(max_length=30)