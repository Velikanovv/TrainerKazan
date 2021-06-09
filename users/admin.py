from django.contrib import admin

# Register your models here.
from .models import Route, Reward, IndicatorsBlock, IndicatorsExercise, IndicatorsExerciseResult, User, IndicatorsMainStatics, IndicatorsExStatics


admin.site.register(Route)
admin.site.register(Reward)
admin.site.register(IndicatorsBlock)
admin.site.register(IndicatorsExercise)
admin.site.register(IndicatorsExerciseResult)
admin.site.register(User)
admin.site.register(IndicatorsMainStatics)
admin.site.register(IndicatorsExStatics)