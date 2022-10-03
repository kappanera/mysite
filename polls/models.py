import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.png', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

class Contact(models.Model):
    first_name = models.CharField(blank=False, null=False, max_length=100)
    last_name = models.CharField(default=None, blank=True, null=True, max_length=100)
    phone = models.CharField(default=None, blank=True, null=True, max_length=100)
    email = models.EmailField(default=None, blank=True, null=True, max_length = 254)
    avatar = models.ImageField(default='default.png', upload_to='contact_images')
    info = models.TextField(default=None, blank=True, null=True)
    
    def __str__(self):
        return self.first_name + ' ' + str(self.last_name or '')

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

    class Meta:
        ordering = ['last_name', 'first_name']

class PersonalContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' - ' + self.contact.first_name + ' ' + str(self.contact.last_name or '')

class WorkContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' - ' + self.contact.first_name + ' ' + str(self.contact.last_name or '')
