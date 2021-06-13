from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from users.models import User, Reward, IndicatorsBlock,IndicatorsExercise, IndicatorsExerciseResult, IndicatorsExStatics, IndicatorsMainStatics
from core.models import Team, LessonsBlock, Lesson, HomeWork, LessonBlockRating, DoneHomeWork

import random
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import datetime as DT
from decimal import Decimal

def main(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    if request.method == 'GET':
        if request.user.is_authenticated:
            team = request.user.user_team.first()
            all_hw = HomeWork.objects.filter(team=team).count()
            done_hw = DoneHomeWork.objects.filter(user=request.user).count()
            ind_blocks = IndicatorsBlock.objects.all()
            main_stat = IndicatorsMainStatics.objects.filter(user_main_statics=request.user).all()
            rewards = Reward.objects.filter()
            percs = []
            i = 0
            for bl in main_stat:
                percs.append(int(350 + (315 - (325 / 100 * int(bl.result)))))
                i += 1
            return render(request, 'player/player.html', {'team': team, 'all_hw': all_hw, 'done_hw': done_hw, 'ind_blocks': ind_blocks,'user': request.user, 'main_stat': main_stat, 'percs': percs})
        else:
            return redirect('signin')

def p(request, pk):
    if not request.user.is_authenticated:
        return redirect('signin')
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = User.objects.filter(pk=pk).first()
            team = user.user_team.first()
            all_hw = HomeWork.objects.filter(team=team).count()
            done_hw = DoneHomeWork.objects.filter(user=user).count()
            ind_blocks = IndicatorsBlock.objects.all()
            main_stat = IndicatorsMainStatics.objects.filter(user_main_statics=user).all()
            percs = []
            i = 0
            for bl in main_stat:
                percs.append(int(350 + (315 - (325 / 100 * int(bl.result)))))
                i += 1
            return render(request, 'player/player.html', {'team': team, 'all_hw': all_hw, 'done_hw': done_hw, 'ind_blocks': ind_blocks,'user': user, 'main_stat': main_stat, 'percs': percs})
        else:
            return redirect('signin')

def team(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    if request.method == 'GET':
        if request.user.is_authenticated:
            team = request.user.user_team.first()
            return render(request, 'player/team.html', {'team': team})
        else:
            return redirect('signin')

def cabinet(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'player/cabinet.html', {})
        else:
            return redirect('signin')
    else:
        if request.user.is_authenticated:
            if request.POST['action'] == 'photo':
                try:
                    if 'img' in request.FILES:
                        photo = request.FILES.get('img')
                        user = request.user
                        user.pic.delete()
                        user.pic = photo
                        user.save()
                        return redirect('player_main')
                    else:
                        return render(request, 'player/cabinet.html', {'error': "yes", 'errort': "Выберете фото"})
                except Exception as e:
                    return render(request, 'player/cabinet.html', {'error': "yes", 'errort': "Системная ошибка: CAB-1"})
            if request.POST['action'] == 'data':
                try:
                    name = request.POST["name"]
                    surname = request.POST["surname"]
                    patronymic = request.POST["patronymic"]
                    user = request.user
                    user.name = name
                    user.surname = surname
                    user.patronymic = patronymic
                    user.save()
                    return redirect('player_cabinet')
                except Exception as e:
                    return render(request, 'player/cabinet.html', {'error': "yes", 'errort': "Системная ошибка: CAB-2"})
            if request.POST['action'] == 'pass':
                try:
                    passw = request.POST["pass"]
                    passws = request.POST["pass2"]
                    user = request.user
                    if passw == passws and len(passw) >= 6:
                        user.password = make_password(passw)
                        user.c_pass = 'Изменен пользователем'
                        user.save()
                        return redirect('player_cabinet')
                    else:
                        return render(request, 'player/cabinet.html', {'error': "yes",'errort': "Пароли не совадают или длина пароля меньше 6 символов"})
                except Exception as e:
                    return render(request, 'player/cabinet.html', {'error': "yes", 'errort': "Системная ошибка: CAB-3"})


def homework(request, pk):
    if not request.user.is_authenticated:
        return redirect('signin')
    homework = HomeWork.objects.filter(pk=pk).first()
    usr = request.user
    if request.method == 'GET':
        if request.user.is_authenticated:
            done_hw = DoneHomeWork.objects.filter(user=usr, homework=homework).first()
            return render(request, 'player/homework.html', {'usr': usr, 'homework': homework, 'done_hw': done_hw })
        else:
            return redirect('signin')
    else:
        if request.user.is_authenticated:
            if request.POST['action'] == 'create':
                try:
                    if 'img' in request.FILES:
                        video = request.FILES.get('img')
                        done_hw = DoneHomeWork.objects.filter(user=usr, homework=homework)
                        if done_hw.exists():
                            done_hw.delete()
                            new = DoneHomeWork.objects.create(user=usr, homework=homework)
                            new.video=video
                            new.save()
                            homework.not_done.remove(usr)
                            homework.done.add(usr)
                            homework.save()
                        else:
                            new = DoneHomeWork.objects.create(user=usr, homework=homework)
                            new.video=video
                            new.save()
                            homework.not_done.remove(usr)
                            homework.done.add(usr)
                            homework.save()
                    return redirect('player_homework', pk)
                except Exception as e:
                    return redirect('player_homework', pk)

def homeworks(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    if request.method == 'GET':
        if request.user.is_authenticated:
            usr = request.user
            team = request.user.user_team.first()
            homeworks = HomeWork.objects.filter(team=team).all().order_by('-date')
            done_hw = DoneHomeWork.objects.filter(user=usr).all()
            return render(request, 'player/homeworks.html', {'usr': usr, 'homeworks': homeworks, 'done_hw': done_hw })
        else:
            return redirect('signin')

def my_way(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    if request.method == 'GET':
        if request.user.is_authenticated:
            usr = request.user
            team = request.user.user_team.first()
            lessons = LessonsBlock.objects.filter(team=team).order_by('-date')
            ratings = LessonBlockRating.objects.filter(user=usr)
            return render(request, 'player/tasks.html', {'usr': usr, 'lessons': lessons,'ratings': ratings})
        else:
            return redirect('signin')

def way(request, pk):
    if not request.user.is_authenticated:
        return redirect('signin')
    if request.method == 'GET':
        if request.user.is_authenticated:
            usr = request.user
            team = request.user.user_team.first()
            lesson = LessonsBlock.objects.filter(pk=pk, team=team).first()
            lessons = Lesson.objects.filter(lessonblock=lesson).all()
            ratings = LessonBlockRating.objects.filter(user=usr)
            return render(request, 'player/task.html', {'usr': usr, 'lessons': lessons, 'lesson': lesson,'ratings': ratings})
        else:
            return redirect('signin')