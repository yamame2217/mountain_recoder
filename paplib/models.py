from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Mountain(models.Model):
    """山の情報を格納するモデル"""
    name = models.CharField('山名', max_length=100)
    prefecture = models.CharField('都道府県', max_length=50)
    elevation = models.IntegerField('標高')

    def __str__(self):
        return self.name


class ClimbRecord(models.Model):
    """登山記録を格納するモデル"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ユーザー')
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE, verbose_name='山')
    climb_date = models.DateField('登った日')
    comment = models.TextField('感想・コメント', blank=True, null=True)
    created_at = models.DateTimeField('作成日', auto_now_add=True)

    def __str__(self):
        return f'{self.mountain.name} ({self.user.username})'