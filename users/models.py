from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.contrib.auth.models import PermissionsMixin
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Adjust, ResizeToFill
from phonenumber_field.modelfields import PhoneNumberField
import random


def users_pic_path(instance, filename):
    return 'users/%s/pic/%s' % (str(instance.username), filename)

def rewards_pic_path(instance, filename):
    return 'rewards/%s/pic/%s' % (str(instance.pk), filename)

class Route(models.Model):
    name = models.CharField(max_length=100)
    total_lessons = models.PositiveIntegerField(default=1)
    attended_lessons = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Reward(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    pic = models.ImageField(upload_to=rewards_pic_path, default='rewards/default_pic.jpg')
    pic_small = ImageSpecField(processors=[ResizeToFill(75, 75)], source='pic', format='JPEG', options={'quality': 100})

    def __str__(self):
        return self.name

class IndicatorsBlock(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            super(IndicatorsBlock, self).save(*args, **kwargs)
            users = User.objects.filter(role=1).all()
            for usr in users:
                main = IndicatorsMainStatics.objects.create(block=self)
                main.user_main_statics.add(usr)
                main.save()
            super(IndicatorsBlock, self).save()
        else:
            super(IndicatorsBlock, self).save(*args, **kwargs)

class IndicatorsExercise(models.Model):
    block = models.ForeignKey(IndicatorsBlock, related_name='indicators_exercise', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    measure_unit = models.CharField(max_length=50)
    best_result = models.DecimalField(max_digits=99999, decimal_places=2, default=0)

    NO_VECTOR = 1
    IS_VECTOR = 2

    VECTOR_CHOICES = (
        (NO_VECTOR, 'Без вектора'),
        (IS_VECTOR, 'Вектор'),
    )
    vector = models.PositiveSmallIntegerField(choices=VECTOR_CHOICES, default=1)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            super(IndicatorsExercise, self).save(*args, **kwargs)
            users = User.objects.filter(role=1).all()
            for usr in users:
                mainSt = IndicatorsMainStatics.objects.filter(user_main_statics=usr, block=self.block).first()
                main = IndicatorsExStatics.objects.create(main=mainSt, indicator=self)
                main.user_ex_statics.add(usr)
                main.save()
            super(IndicatorsExercise, self).save()
        else:
            super(IndicatorsExercise, self).save(*args, **kwargs)

class IndicatorsExerciseResult(models.Model):
    exercise = models.ForeignKey(IndicatorsExercise, related_name='indicators_exercise_result', on_delete=models.CASCADE, null=True)
    result = models.DecimalField(max_digits=99999, decimal_places=2, default=0)

    def __str__(self):
        return str(self.result)

class IndicatorsMainStatics(models.Model):
    block = models.ForeignKey(IndicatorsBlock, related_name='indicators_main_statics', on_delete=models.CASCADE, null=True)
    result = models.DecimalField(max_digits=99999, decimal_places=2, default=0)

    def __str__(self):
        user = self.user_main_statics.first()
        return str(self.block.name) + ", " + str(user) + ", " + str(self.result)

class IndicatorsExStatics(models.Model):
    main = models.ForeignKey(IndicatorsMainStatics, related_name='indicators_ex_statics', on_delete=models.CASCADE, null=True)
    indicator = models.ForeignKey(IndicatorsExercise, related_name='indicators_ex_statics_e', on_delete=models.CASCADE, null=True)
    result = models.DecimalField(max_digits=99999, decimal_places=2, default=0)

    def __str__(self):
        return str(self.result)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), unique=True, max_length=100)
    email = models.EmailField(_('email address'), blank=True, null=True)

    pic = models.ImageField(upload_to=users_pic_path, default='users/default_pic.jpg')
    pic_small = ImageSpecField(processors=[ResizeToFill(75, 75)], source='pic', format='JPEG', options={'quality': 100})

    name = models.CharField(blank=True, max_length=100)
    surname = models.CharField(blank=True, max_length=100)
    patronymic = models.CharField(blank=True, max_length=100)
    player_number = models.CharField(default='01', max_length=3)
    c_pass = models.CharField(max_length=100, blank=True)

    birthday = models.DateField(blank=True, default=timezone.now)


    rewards = models.ManyToManyField(Reward, related_name='user_rewards', blank=True)
    indicators_results = models.ManyToManyField(IndicatorsExerciseResult, related_name='user_indicators_results', blank=True)
    main_statics = models.ManyToManyField(IndicatorsMainStatics, blank=True, null=True, related_name='user_main_statics')
    ex_statics = models.ManyToManyField(IndicatorsExStatics, blank=True, null=True, related_name='user_ex_statics')


    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    STANDART = 1
    ADMINISTRATOR = 2

    USER_ROLE_CHOICES = (
        (STANDART, 'Ученик'),
        (ADMINISTRATOR, 'Администратор/Тренер'),
    )
    role = models.PositiveSmallIntegerField(choices=USER_ROLE_CHOICES, default=1)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    readonly_fields = [
        'date_joined',
    ]

    objects = CustomUserManager()

    def __str__(self):
        return self.surname + ' ' + self.name + ' ' + self.patronymic