from django.db import models

from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    avatar_url = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    back_url = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    tel = models.CharField(max_length=255, null=True, blank=True)


class Addresss(models.Model):
    #address_id = models.BigIntegerField(primary_key=True)
    address = models.TextField(null=True)

class order(models.Model):
    name = models.TextField()
    desc = models.TextField()


class infodetail(models.Model):
    name1 = models.TextField(null=True)
    price1 = models.TextField(null=True)
    image1 = models.CharField(max_length=255, null=True)
    name2 = models.TextField(null=True)
    price2 = models.TextField(null=True)
    image2 = models.CharField(max_length=255, null=True)


class Store(models.Model):
    name = models.TextField()
    phone = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.TextField()
    desc = models.TextField()


class Cookbook(models.Model):
    cookbook_id = models.BigIntegerField(primary_key=True)  # 主键，bigint
    cookbook_name = models.CharField(max_length=255)  # 菜谱名称，varchar(255)
    food = models.TextField()  # 食材，text
    step = models.TextField()  # 步骤，text
    images = models.CharField(max_length=255)  # 图片链接，varchar(255)
    videos = models.CharField(max_length=255)  # 视频链接，varchar(255)
    preference = models.IntegerField()  # 偏好，int
    likes = models.BooleanField(null=True)
    category = models.TextField(default="推荐")

    def __str__(self):
        return self.cookbook_name

class Communityss(models.Model):
    community_id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=255, default='花花')
    images = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True, null=True)
    content = models.TextField()

    def __str__(self):
        return self.community_id
