from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Adjust, ResizeToFill
from phonenumber_field.modelfields import PhoneNumberField
import random
from users.models import User

def homework_video_path(instance, filename):
    return 'homeworks/%s/video/%s' % (str(instance.pk), filename)

def lessonsblocks_pic_path(instance, filename):
    return 'lessonsblocks/%s/pic/%s' % (str(instance.pk), filename)

def lessons_pic_path(instance, filename):
    return 'lessons/%s/pic/%s' % (str(instance.pk), filename)

def homeworks_pic_path(instance, filename):
    return 'homeworks/%s/pic/%s' % (str(instance.pk), filename)

class Team(models.Model):
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(User, related_name='user_team')

    def __str__(self):
        return self.name

class HomeWork(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    text = models.TextField()

    pic = models.ImageField(upload_to=homeworks_pic_path, default='default_pic.jpg')
    pic_small = ImageSpecField(processors=[ResizeToFill(75, 75)], source='pic', format='JPEG', options={'quality': 100})

    date = models.DateTimeField(default=timezone.now)

    done = models.ManyToManyField(User, related_name='homework_done', blank=True)
    not_done = models.ManyToManyField(User, related_name='homework_not_done', blank=True)

class DoneHomeWork(models.Model):
    user = models.ForeignKey(User, related_name='user_done_homework', on_delete=models.CASCADE)
    homework = models.ForeignKey(HomeWork,related_name='done_homework', on_delete=models.CASCADE)
    video = models.FileField(upload_to=homework_video_path, blank=True, null=True)

    rating = models.PositiveSmallIntegerField(default=0)
    done = models.BooleanField(default=False)
    comment = models.TextField(blank=True)

    date = models.DateTimeField(default=timezone.now)

class LessonsBlock(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()

    pic = models.ImageField(upload_to=lessonsblocks_pic_path, default='default_pic.jpg')
    pic_small = ImageSpecField(processors=[ResizeToFill(75, 75)], source='pic', format='JPEG', options={'quality': 100})

    date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.team.name + ' | ' + self.name

class LessonBlockRating(models.Model):
    block = models.ForeignKey(LessonsBlock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=1, decimal_places=0, default=0)

    def __str__(self):
        return str(self.user) + ' | ' + str(self.block) + ' | ' + str(self.rating)

    def save(self, *args, **kwargs):
        if not self.pk:
            super(LessonBlockRating, self).save(*args, **kwargs)
        else:
            done_l = 0
            all_l = self.block.lessons.count()
            for lesson in self.block.lessons.all():
                if self.user in lesson.done.all():
                    done_l += 1
            self.rating = int(done_l*100/all_l*5/100)
            super(LessonBlockRating, self).save(*args, **kwargs)

class Lesson(models.Model):
    lessonblock = models.ForeignKey(LessonsBlock, related_name='lessons', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()

    pic = models.ImageField(upload_to=lessons_pic_path, default='default_pic.jpg')
    pic_small = ImageSpecField(processors=[ResizeToFill(75, 75)], source='pic', format='JPEG', options={'quality': 100})

    done = models.ManyToManyField(User, related_name='lesson_done', blank=True)
    not_done = models.ManyToManyField(User, related_name='lesson_not_done', blank=True)

    def __str__(self):
        return self.lessonblock.team.name + ' | ' + self.lessonblock.name + ' | ' + self.name