from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Mountain(models.Model):
    name = models.CharField('山名', max_length=100)
    prefecture = models.CharField('都道府県', max_length=50)
    elevation = models.IntegerField('標高')

    def __str__(self):
        return self.name


class ClimbRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ユーザー')
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE, verbose_name='山')
    climb_date = models.DateField('登った日')
    comment = models.TextField('感想・コメント', blank=True, null=True)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    image = models.ImageField('写真', upload_to='photos/', blank=True, null=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    def __str__(self):
        return f'{self.mountain.name} ({self.user.username})'