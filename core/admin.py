from django.contrib import admin

# Register your models here.
from .models import Team, HomeWork, DoneHomeWork, LessonsBlock, Lesson, LessonBlockRating


admin.site.register(Team)
admin.site.register(HomeWork)
admin.site.register(DoneHomeWork)
admin.site.register(LessonsBlock)
admin.site.register(Lesson)
admin.site.register(LessonBlockRating)