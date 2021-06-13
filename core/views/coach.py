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

def new_list_columns(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

def main(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            teams_l = Team.objects.all()
            teams = new_list_columns(teams_l, 3)
            return render(request, 'coach/main.html', {'teams': teams})
        else:
            return redirect('signin')

def team_delete(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            team = Team.objects.filter(pk=pk).first()
            for usr in team.users.all():
                usr.delete()
            homeworks = HomeWork.objects.filter(team=team).all()
            for h in homeworks:
                for d in h.done_homework.all():
                    d.delete()
                h.delete()
            team.delete()
            return redirect('coach_main')
        else:
            return redirect('signin')

def team_create(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            return render(request, 'coach/team_create.html', {})
        else:
            return redirect('signin')
    else:
        if request.user.is_authenticated and request.user.role == 2:
            if request.POST['t_name'] != '':
                team = Team.objects.create(name=request.POST['t_name'])
                team.save()
            return redirect('coach_main')
        else:
            return redirect('signin')

def team_edit(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            team = Team.objects.filter(pk=pk).first()
            return render(request, 'coach/team_edit.html', { 'team': team })
        else:
            return redirect('signin')
    else:
        if request.user.is_authenticated and request.user.role == 2:
            if request.POST['t_name'] != '':
                team = Team.objects.filter(pk=pk).first()
                team.name=request.POST['t_name']
                team.save()
            return redirect('coach_main')
        else:
            return redirect('signin')

def team_lessons_blocks_lessons(request, pk, bpk):
    team = Team.objects.filter(pk=pk).first()
    block = LessonsBlock.objects.filter(pk=bpk).first()
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            return render(request, 'coach/team_lesson_block_lessons.html', {'team': team, 'c_block': block })
        else:
            return redirect('signin')

def team_lessons_blocks_lessons_visit(request, pk, bpk, lpk):
    team = Team.objects.filter(pk=pk).first()
    block = LessonsBlock.objects.filter(pk=bpk).first()
    lesson = Lesson.objects.filter(pk=lpk).first()
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            return render(request, 'coach/team_lesson_block_lessons_done.html', {'team': team, 'c_block': block, 'lesson': lesson })
        else:
            return redirect('signin')
    else:
        if request.user.is_authenticated and request.user.role == 2:
            if 'done' in request.POST:
                try:
                    usr = User.objects.filter(pk=request.POST['done']).first()
                    lesson.done.add(usr)
                    lesson.not_done.remove(usr)
                    lesson.save()
                    lbr = LessonBlockRating.objects.filter(user=usr, block=block).first()
                    lbr.save()
                    return render(request, 'coach/team_lesson_block_lessons_done.html', {'team': team, 'c_block': block, 'lesson': lesson })
                except Exception as e:
                    return render(request, 'coach/team_lesson_block_lessons_done.html', {'team': team, 'c_block': block, 'lesson': lesson })
            elif 'not_done' in request.POST:
                try:
                    usr = User.objects.filter(pk=request.POST['not_done']).first()
                    lesson.done.remove(usr)
                    lesson.not_done.add(usr)
                    lesson.save()
                    lbr = LessonBlockRating.objects.filter(user=usr, block=block).first()
                    lbr.save()
                    return render(request, 'coach/team_lesson_block_lessons_done.html', {'team': team, 'c_block': block, 'lesson': lesson })
                except Exception as e:
                    return render(request, 'coach/team_lesson_block_lessons_done.html', {'team': team, 'c_block': block, 'lesson': lesson })

def team_lessons_blocks_lessons_delete(request, pk, bpk, lpk):
    team = Team.objects.filter(pk=pk).first()
    block = LessonsBlock.objects.filter(pk=bpk).first()
    lesson = Lesson.objects.filter(pk=lpk).first()
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            lesson.delete()
            return redirect('coach_team_lessons_blocks_lessons', team.pk, block.pk)
        else:
            return redirect('signin')

def team_lessons_blocks_lessons_edit(request, pk, bpk, lpk):
    team = Team.objects.filter(pk=pk).first()
    block = LessonsBlock.objects.filter(pk=bpk).first()
    lesson = Lesson.objects.filter(pk=lpk).first()
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            return render(request, 'coach/team_lesson_block_lessons_edit.html', {'team': team, 'c_block': block, 'lesson': lesson })
        else:
            return redirect('signin')
    else:
        if request.user.is_authenticated and request.user.role == 2:
            if request.POST['action'] == 'create':
                try:
                    if 'img' in request.FILES:
                        pic = request.FILES.get('img')
                        name = request.POST['name']
                        descr = request.POST['descr']
                        new = lesson
                        new.name=name
                        new.description=descr
                        new.pic=pic
                        new.save()
                    else:
                        name = request.POST['name']
                        descr = request.POST['descr']
                        new = lesson
                        new.name=name
                        new.description=descr
                        new.save()
                    return JsonResponse({}, status=200)
                except Exception as e:
                    return JsonResponse({'errors': 'Ошибка при редактировании: ' + e.args[0]}, status=400)

def team_lessons_blocks_lessons_create(request, pk, bpk):
    team = Team.objects.filter(pk=pk).first()
    block = LessonsBlock.objects.filter(pk=bpk).first()
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            return render(request, 'coach/team_lesson_block_lessons_create.html', {'team': team, 'c_block': block })
        else:
            return redirect('signin')
    else:
        if request.user.is_authenticated and request.user.role == 2:
            if request.POST['action'] == 'create':
                try:
                    if 'img' in request.FILES:
                        pic = request.FILES.get('img')
                        name = request.POST['name']
                        descr = request.POST['descr']
                        new = Lesson.objects.create(name=name, description=descr, lessonblock=block, pic=pic)
                        for usr in team.users.all():
                            new.not_done.add(usr)
                        new.save()
                    else:
                        name = request.POST['name']
                        descr = request.POST['descr']
                        new = Lesson.objects.create(name=name, description=descr, lessonblock=block)
                        for usr in team.users.all():
                            new.not_done.add(usr)
                        new.save()
                    return JsonResponse({}, status=200)
                except Exception as e:
                    return JsonResponse({'errors': 'Ошибка при создании: ' + e.args[0]}, status=400)

def team_lessons_blocks_delete(request, pk, bpk):
    team = Team.objects.filter(pk=pk).first()
    block = LessonsBlock.objects.filter(pk=bpk).first()
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            for usr in team.users.all():
                rat = LessonBlockRating.objects.filter(user=usr, block=block).first()
                rat.delete()
            for lesson in block.lessons.all():
                lesson.delete()
            for r in LessonBlockRating.objects.filter(block=block):
                r.delete()
            block.delete()

            return redirect('coach_team_lessons_blocks', team.pk)
        else:
            return redirect('signin')

def team_lessons_blocks_edit(request, pk, bpk):
    team = Team.objects.filter(pk=pk).first()
    block = LessonsBlock.objects.filter(pk=bpk).first()
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            return render(request, 'coach/team_lesson_block_edit.html', {'team': team, 'c_block': block })
        else:
            return redirect('signin')
    else:
        if request.user.is_authenticated and request.user.role == 2:
            if request.POST['action'] == 'create':
                try:
                    if 'img' in request.FILES:
                        pic = request.FILES.get('img')
                        name = request.POST['name']
                        descr = request.POST['descr']
                        new = LessonsBlock.objects.filter(pk=bpk).first()
                        new.name = name
                        new.pic = pic
                        new.description=descr
                        new.save()
                        for usr in team.users.all():
                            if not LessonBlockRating.objects.filter(user=usr, block=new).exists():
                                LessonBlockRating.objects.create(user=usr, block=new,rating=0)
                    else:
                        name = request.POST['name']
                        descr = request.POST['descr']
                        new = LessonsBlock.objects.filter(pk=bpk).first()
                        new.name = name
                        new.description=descr
                        new.save()
                        for usr in team.users.all():
                            if not LessonBlockRating.objects.filter(user=usr, block=new).exists():
                                LessonBlockRating.objects.create(user=usr, block=new,rating=0)
                    return JsonResponse({}, status=200)
                except Exception as e:
                    return JsonResponse({'errors': 'Ошибка при изменении блока: ' + e.args[0]}, status=400)

def team_lessons_blocks_create(request, pk):
    team = Team.objects.filter(pk=pk).first()
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            return render(request, 'coach/team_lesson_block_create.html', {'team': team})
        else:
            return redirect('signin')
    else:
        if request.user.is_authenticated and request.user.role == 2:
            if request.POST['action'] == 'create':
                try:
                    if 'img' in request.FILES:
                        pic = request.FILES.get('img')
                        name = request.POST['name']
                        descr = request.POST['descr']
                        count = int(request.POST['count'])
                        new = LessonsBlock.objects.create(name=name, description=descr, team=team, pic=pic)
                        new.save()
                        for i in range(count):
                            lsn = Lesson.objects.create(name=('Урок ' + str(i+1)), description=('Блок ' + team.name + ', Урок ' + str(i+1) + '.'), lessonblock=new)
                            for usr in team.users.all():
                                lsn.not_done.add(usr)
                        for usr in team.users.all():
                            LessonBlockRating.objects.create(user=usr, block=new,rating=0)
                    else:
                        name = request.POST['name']
                        descr = request.POST['descr']
                        count = int(request.POST['count'])
                        new = LessonsBlock.objects.create(name=name, description=descr, team=team)
                        new.save()
                        for i in range(count):
                            lsn = Lesson.objects.create(name=('Урок ' + str(i+1)), description=('Блок ' + team.name + ', Урок ' + str(i+1) + '.'), lessonblock=new)
                            for usr in team.users.all():
                                lsn.not_done.add(usr)
                        for usr in team.users.all():
                            LessonBlockRating.objects.create(user=usr, block=new,rating=0)
                    return JsonResponse({}, status=200)
                except Exception as e:
                    return JsonResponse({'errors': 'Ошибка при создании пользвателя: ' + e.args[0]}, status=400)

def users(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            users = User.objects.filter(role=1).all()
            return render(request, 'coach/users.html', {'users': users})
        else:
            return redirect('signin')

def team_users_delete(request, pk, upk):
    team = Team.objects.filter(pk=pk).first()
    usr = User.objects.filter(pk=upk).first()
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            for r in usr.indicators_results.all():
                r.delete()
            for ex in usr.ex_statics.all():
                ex.delete()
            for ms in usr.main_statics.all():
                ms.delete()
            usr = User.objects.filter(pk=upk).first().delete()
            return redirect('coach_team', team.pk)
        else:
            return redirect('signin')

def team_users_create(request, pk):
    team = Team.objects.filter(pk=pk).first()
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            return render(request, 'coach/team_user_create.html', {'team': team})
        else:
            return redirect('signin')
    else:
        if request.user.is_authenticated and request.user.role == 2:
            if request.POST['action'] == 'create':
                try:
                    login = request.POST['login'].lower()
                    name = request.POST['name']
                    surname = request.POST['surname']
                    patronymic = request.POST['patronymic']
                    password = request.POST['password']
                    number = request.POST['number']
                    if password == '':
                        letters = 'QWERTYUIOPASDFHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890-_'
                        code = ''.join(random.choice(letters) for i in range(7))
                        password = code
                    date = DT.datetime.strptime(request.POST['date'], '%m/%d/%Y')
                    if 'img' in request.FILES:
                        pic = request.FILES.get('img')
                        new = User.objects.create(username=login,password=make_password(password), c_pass=password, name=name, surname=surname, patronymic=patronymic, birthday=date, pic=pic, role=1, player_number=number)
                        new.save()
                        team.users.add(new)
                        team.save()
                        blocks = IndicatorsBlock.objects.all()
                        for bl in blocks:
                            ind = IndicatorsMainStatics.objects.create(block=bl)
                            ind.save()
                            new.main_statics.add(ind)
                            new.save()
                            for i in bl.indicators_exercise.all():
                                ins = IndicatorsExStatics.objects.create(main=ind, indicator=i)
                                ins.save()
                                new.ex_statics.add(ins)
                                new.save()
                    else:
                        new = User.objects.create(username=login,password=make_password(password), c_pass=password, name=name, surname=surname, patronymic=patronymic, birthday=date, role=1, player_number=number)
                        new.save()
                        team.users.add(new)
                        team.save()
                        blocks = IndicatorsBlock.objects.all()
                        for bl in blocks:
                            ind = IndicatorsMainStatics.objects.create(block=bl)
                            ind.save()
                            new.main_statics.add(ind)
                            new.save()
                            for i in bl.indicators_exercise.all():
                                ins = IndicatorsExStatics.objects.create(main=ind, indicator=i)
                                ins.save()
                                new.ex_statics.add(ins)
                                new.save()
                    return JsonResponse({}, status=200)
                except Exception as e:
                    return JsonResponse({'errors': 'Ошибка при создании пользвателя: ' + e.args[0]}, status=400)

def team_users_edit(request, pk, upk):
    team = Team.objects.filter(pk=pk).first()
    usr = User.objects.filter(pk=upk).first()
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            return render(request, 'coach/team_user_edit.html', {'team': team, 'usr': usr })
        else:
            return redirect('signin')
    else:
        if request.user.is_authenticated and request.user.role == 2:
            if request.POST['action'] == 'create':
                try:
                    login = request.POST['login'].lower()
                    name = request.POST['name']
                    surname = request.POST['surname']
                    patronymic = request.POST['patronymic']
                    password = request.POST['password']
                    number = request.POST['number']
                    if password == '':
                        letters = 'QWERTYUIOPASDFHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890-_'
                        code = ''.join(random.choice(letters) for i in range(7))
                        password = code
                    date = DT.datetime.strptime(request.POST['date'], '%m/%d/%Y')
                    if 'img' in request.FILES:
                        pic = request.FILES.get('img')
                        usr.username=login
                        if password != 'Изменен пользователем':
                            usr.password=make_password(password)
                            usr.c_pass=password
                        usr.name=name
                        usr.surname=surname
                        usr.patronymic=patronymic
                        usr.birthday=date
                        usr.pic=pic
                        usr.role=1
                        usr.player_number=number
                        usr.save()
                    else:
                        usr.username=login
                        if password != 'Изменен пользователем':
                            usr.password=make_password(password)
                            usr.c_pass=password
                        usr.name=name
                        usr.surname=surname
                        usr.patronymic=patronymic
                        usr.birthday=date
                        usr.role=1
                        usr.player_number=number
                        usr.save()
                    return JsonResponse({}, status=200)
                except Exception as e:
                    return JsonResponse({'errors': 'Ошибка при создании пользвателя: ' + e.args[0]}, status=400)

def trainers(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            trainers = User.objects.filter(role=2).all()
            return render(request, 'coach/trainers.html', {'users': trainers})
        else:
            return redirect('signin')

def trainers_edit(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            trainer = User.objects.filter(pk=pk).first()
            return render(request, 'coach/trainers_edit.html', {'trainer': trainer})
        else:
            return redirect('signin')
    else:
        if request.user.is_authenticated and request.user.role == 2:
            if request.POST['action'] == 'create':
                try:
                    login = request.POST['login'].lower()
                    name = request.POST['name']
                    surname = request.POST['surname']
                    patronymic = request.POST['patronymic']
                    password = request.POST['password']
                    if password == '':
                        letters = 'QWERTYUIOPASDFHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890-_'
                        code = ''.join(random.choice(letters) for i in range(7))
                        password = code
                    date = DT.datetime.strptime(request.POST['date'], '%m/%d/%Y')
                    usr = User.objects.filter(pk=pk).first()
                    if 'img' in request.FILES:
                        pic = request.FILES.get('img')
                        usr.username=login
                        usr.password=make_password(password)
                        usr.c_pass=password
                        usr.name=name
                        usr.surname=surname
                        usr.patronymic=patronymic
                        usr.birthday=date
                        usr.pic=pic
                        usr.role=2
                        usr.save()
                    else:
                        usr.username=login
                        usr.password=make_password(password)
                        usr.c_pass=password
                        usr.name=name
                        usr.surname=surname
                        usr.patronymic=patronymic
                        usr.birthday=date
                        usr.role=2
                        usr.save()
                    return JsonResponse({}, status=200)
                except Exception as e:
                    return JsonResponse({'errors': 'Ошибка при создании пользвателя: ' + e.args[0]}, status=400)

def trainers_create(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            return render(request, 'coach/trainers_create.html', {})
        else:
            return redirect('signin')
    else:
        if request.user.is_authenticated and request.user.role == 2:
            if request.POST['action'] == 'create':
                try:
                    login = request.POST['login'].lower()
                    name = request.POST['name']
                    surname = request.POST['surname']
                    patronymic = request.POST['patronymic']
                    password = request.POST['password']
                    if password == '':
                        letters = 'QWERTYUIOPASDFHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890-_'
                        code = ''.join(random.choice(letters) for i in range(7))
                        password = code
                    date = DT.datetime.strptime(request.POST['date'], '%m/%d/%Y')
                    if 'img' in request.FILES:
                        pic = request.FILES.get('img')
                        new = User.objects.create(username=login,password=make_password(password), c_pass=password, name=name, surname=surname, patronymic=patronymic, birthday=date, pic=pic, role=2)
                        new.save()
                    else:
                        new = User.objects.create(username=login,password=make_password(password), c_pass=password, name=name, surname=surname, patronymic=patronymic, birthday=date, role=2)
                        new.save()
                    return JsonResponse({}, status=200)
                except Exception as e:
                    return JsonResponse({'errors': 'Ошибка при создании пользвателя: ' + e.args[0]}, status=400)

def indicators(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            indicators_blocks = IndicatorsBlock.objects.all().order_by('name')
            indicators = IndicatorsExercise.objects.all().order_by('name')
            return render(request, 'coach/indicators.html', {'indicators_blocks': indicators_blocks, 'indicators': indicators})
        else:
            return redirect('signin')

def indicators_delete(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            indicator = IndicatorsExercise.objects.filter(pk=pk)
            if indicator.exists():
                indicator.first().delete()
            return redirect('coach_indicators')
        else:
            return redirect('signin')

def indicators_edit(request, pk, epk):
    indicators_exercise = IndicatorsExercise.objects.filter(pk=epk)
    indicators_block = IndicatorsBlock.objects.filter(pk=pk)
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            if indicators_block.exists():
                exercise = indicators_exercise.first()
                block = indicators_block.first()
                return render(request, 'coach/indicators_edit.html', {'i_block': block, 'exercise': exercise})
            else:
                return redirect('coach_indicators')
        else:
            return redirect('signin')
    else:
        if request.user.is_authenticated and request.user.role == 2:
            if request.POST['action'] == 'create':
                try:
                    title = request.POST['title']
                    mesuare = request.POST['mesuare']
                    best = request.POST['best']
                    vectors = request.POST['vector']
                    if vectors == 'true':
                        vector = 2
                    else:
                        vector = 1
                    if indicators_exercise.exists():
                        i = indicators_exercise.first()
                        i.name = title
                        i.measure_unit = mesuare
                        i.best_result = Decimal(best)
                        i.vector = vector
                        i.save()
                        return JsonResponse({}, status=200)
                    else:
                        return JsonResponse({'errors': 'Нет такого блока'}, status=400)
                except:
                    return JsonResponse({'errors': 'Ошибка при создании'}, status=400)

def indicators_create(request, pk):
    indicators_block = IndicatorsBlock.objects.filter(pk=pk)
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            if indicators_block.exists():
                return render(request, 'coach/indicators_create.html', {'indicators_block': indicators_block.first()})
            else:
                return redirect('coach_indicators')
        else:
            return redirect('signin')
    else:
        if request.user.is_authenticated and request.user.role == 2:
            if request.POST['action'] == 'create':
                try:
                    title = request.POST['title']
                    mesuare = request.POST['mesuare']
                    best = request.POST['best']
                    vectors = request.POST['vector']
                    if vectors == 'true':
                        vector = 2
                    else:
                        vector = 1
                    if indicators_block.exists():
                        indicators_block = indicators_block.first()
                        new = IndicatorsExercise.objects.create(name=title, measure_unit=mesuare, best_result=best, vector=vector, block=indicators_block)
                        new.save()
                        return JsonResponse({}, status=200)
                    else:
                        return JsonResponse({'errors': 'Нет такого блока'}, status=400)
                except:
                    return JsonResponse({'errors': 'Ошибка при создании'}, status=400)


def rewards(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            rewards = Reward.objects.all().order_by('name')
            return render(request, 'coach/rewards.html', {'rewards': rewards})
        else:
            return redirect('signin')

def rewards_delete(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            reward = Reward.objects.filter(pk=pk)
            if reward.exists():
                reward = reward.first()
                reward.delete()
            return redirect('coach_rewards')
        else:
            return redirect('signin')

def rewards_edit(request, pk):
    if not request.user.is_authenticated and request.user.role == 2:
        return redirect('signin')

    reward = Reward.objects.filter(pk=pk)
    if request.method == 'GET':
        if request.user.is_authenticated:
            if not reward.exists():
                return redirect('coach_rewards')
            reward = reward.first()
            return render(request, 'coach/rewards_edit.html', {'reward': reward})
        else:
            return redirect('signin')
    elif request.method == 'POST':
        reward = reward.first()
        if request.POST['action'] == 'create':
            try:
                title = request.POST['title']
                descr = request.POST['descr']
                if 'img' in request.FILES:
                    pic = request.FILES.get('img')
                    reward.name = title
                    reward.description = descr
                    reward.pic = pic
                    reward.save()
                else:
                    reward.name = title
                    reward.description = descr
                    reward.save()
                return JsonResponse({}, status=200)
            except:
                return JsonResponse({'errors': 'Ошибка при изменении'}, status=400)

def rewards_create(request):
    if not request.user.is_authenticated and request.user.role == 2:
        return redirect('signin')

    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            return render(request, 'coach/rewards_create.html', {})
        else:
            return redirect('signin')
    elif request.method == 'POST':
        if request.POST['action'] == 'create':
            try:
                title = request.POST['title']
                descr = request.POST['descr']
                if 'img' in request.FILES:
                    pic = request.FILES.get('img')
                    new = Reward.objects.create(name=title, description=descr, pic=pic)
                    new.save()
                else:
                    new = Reward.objects.create(name=title, description=descr)
                    new.save()
                return JsonResponse({}, status=200)
            except:
                return JsonResponse({'errors': 'Ошибка при создании'}, status=400)

def team(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            team_l = Team.objects.filter(pk=pk)
            if not team_l.exists():
                return redirect('coach_main')
            team = team_l.first()
            users = team.users.all()
            lessons_blocks = LessonsBlock.objects.filter(team=team).all()
            return render(request, 'coach/team.html', {'team': team, 'users': users,'lessons_blocks': lessons_blocks})
        else:
            return redirect('signin')

def team_lessons_blocks(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            team_l = Team.objects.filter(pk=pk)
            if not team_l.exists():
                return redirect('coach_main')
            team = team_l.first()
            users = team.users.all()
            lessons_blocks = LessonsBlock.objects.filter(team=team).order_by('-date').all()
            return render(request, 'coach/team_lessson_block.html', {'team': team, 'users': users,'lessons_blocks': lessons_blocks})
        else:
            return redirect('signin')

def team_indicators_add(request, pk, ipk):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            team_l = Team.objects.filter(pk=pk)
            if not team_l.exists():
                return redirect('coach_main')
            team = team_l.first()
            users = User.objects.filter(user_team=team).order_by('name').all()
            indicator = IndicatorsExercise.objects.filter(pk=ipk).first()
            return render(request, 'coach/team_indicators_add.html', {'indicator': indicator, 'team': team, 'users': users })
        else:
            return redirect('signin')
    else:
        if request.user.is_authenticated and request.user.role == 2:
            team_l = Team.objects.filter(pk=pk)
            if not team_l.exists():
                return redirect('coach_main')
            team = team_l.first()
            user = User.objects.filter(pk=int(request.POST['user'])).first()

            indicator = IndicatorsExercise.objects.filter(pk=ipk).first()
            result = Decimal(request.POST['result'])
            if indicator.vector == 2:
                if result < indicator.best_result:
                    indicator.best_result = result
                    indicator.save()
            else:
                if result > indicator.best_result:
                    indicator.best_result = result
                    indicator.save()
            nr = IndicatorsExerciseResult.objects.create(exercise=indicator, result=result)
            nr.save()
            user.indicators_results.add(nr)
            users = User.objects.filter(user_team=team).order_by('name').all()

            ex = indicator
            block = ex.block
            res = 0
            if ex.vector == 2:
                res = (ex.best_result * 100) / result
            else:
                res = (result * 100) / ex.best_result
            exStat = IndicatorsExStatics.objects.filter(indicator=ex, user_ex_statics=user).all()
            for stat in exStat:
                if stat in user.ex_statics.all():
                    stat.result = int(res)
                    stat.save()
                    res = 0
                    all_st = IndicatorsExStatics.objects.filter(main=stat.main, user_ex_statics=user).all()
                    for st in all_st:
                        res += st.result
                    res = res / all_st.count()
                    stat.main.result = int(res)
                    stat.main.save()



            return render(request, 'coach/team_indicators_add.html', {'indicator': indicator, 'team': team, 'users': users, 'success': 'success' })
        else:
            return redirect('signin')





def team_indicators_static(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            team_l = Team.objects.filter(pk=pk)
            if not team_l.exists():
                return redirect('coach_main')
            team = team_l.first()
            users = User.objects.filter(user_team=team).order_by('name').all()
            indicators_blocks = IndicatorsBlock.objects.all().order_by('name')
            indicators = IndicatorsExercise.objects.all().order_by('name')
            return render(request, 'coach/team_indicators_static.html', {'indicators_blocks': indicators_blocks, 'indicators': indicators, 'team': team, 'users': users})
        else:
            return redirect('signin')

def team_indicators(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            team_l = Team.objects.filter(pk=pk)
            if not team_l.exists():
                return redirect('coach_main')
            team = team_l.first()
            users = User.objects.filter(user_team=team).order_by('name').all()
            indicators_blocks = IndicatorsBlock.objects.all().order_by('name')
            indicators = IndicatorsExercise.objects.all().order_by('name')
            return render(request, 'coach/team_indicators.html', {'indicators_blocks': indicators_blocks, 'indicators': indicators, 'team': team})
        else:
            return redirect('signin')


def team_rewards(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            team_l = Team.objects.filter(pk=pk)
            if not team_l.exists():
                return redirect('coach_main')
            team = team_l.first()
            users = User.objects.filter(user_team=team).order_by('name').all()
            return render(request, 'coach/team_rewards.html', {'team': team,'users': users})
        else:
            return redirect('signin')

def team_rewards_delete(request, pk, rpk, upk):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            team_l = Team.objects.filter(pk=pk)
            if not team_l.exists():
                return redirect('coach_main')
            team = team_l.first()
            usr = User.objects.filter(pk=upk).first()
            reward = Reward.objects.filter(pk=rpk).first()
            if reward in usr.rewards.all():
                if usr in team.users.all():
                    usr.rewards.remove(reward)
            return redirect('coach_team_rewards', team.pk )
        else:
            return redirect('signin')

def team_rewards_add(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            team_l = Team.objects.filter(pk=pk)
            if not team_l.exists():
                return redirect('coach_main')
            team = team_l.first()
            users = User.objects.filter(user_team=team).order_by('name').all()
            all_rewards = Reward.objects.all()
            return render(request, 'coach/team_rewards_add.html', {'team': team,'users': users, 'all_rewards': all_rewards})
        else:
            return redirect('signin')
    else:
        if request.user.is_authenticated and request.user.role == 2:
            team_l = Team.objects.filter(pk=pk)
            if not team_l.exists():
                return redirect('coach_main')
            team = team_l.first()
            print(request.POST)
            if request.POST['r_type'] == 'all_team':
                users = User.objects.filter(user_team=team).order_by('name').all()
                reward = Reward.objects.filter(pk=request.POST['reward']).first()
                for usr in users:
                    usr.rewards.add(reward)
            if request.POST['r_type'] == 'some_team':
                users = User.objects.filter(user_team=team).order_by('name').all()
                reward = Reward.objects.filter(pk=request.POST['reward']).first()
                for usr in users:
                    if ('user_check_' + str(usr.pk)) in request.POST:
                        if request.POST['user_check_' + str(usr.pk)] == 'on':
                            usr.rewards.add(reward)
            return redirect('coach_team_rewards', team.pk)
        else:
            return redirect('signin')


def team_homeworks(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            team_l = Team.objects.filter(pk=pk)
            if not team_l.exists():
                return redirect('coach_main')
            team = team_l.first()
            homeworks = HomeWork.objects.filter(team=team).order_by('-date').all()
            return render(request, 'coach/team_homework.html', {'team': team,'homeworks': homeworks})
        else:
            return redirect('signin')

def team_homeworks_delete(request, pk, hpk):
    if not request.user.is_authenticated and request.user.role == 2:
        return redirect('signin')

    team_l = Team.objects.filter(pk=pk)
    if not team_l.exists():
        return redirect('coach_main')
    team = team_l.first()

    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            work = HomeWork.objects.filter(pk=hpk).first()
            for w in work.done_homework.all():
                w.delete()
            work.delete()
            return redirect('coach_team_homeworks', team.pk)
        else:
            return redirect('signin')

def team_homeworks_work(request, pk, hpk):
    if not request.user.is_authenticated and request.user.role == 2:
        return redirect('signin')
    team_l = Team.objects.filter(pk=pk)
    if not team_l.exists():
        return redirect('coach_main')
    team = team_l.first()
    work = HomeWork.objects.filter(pk=hpk).first()

    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            all_work = DoneHomeWork.objects.filter(homework=work).all()
            rat_work = []
            nrat_work = []
            for wrk in all_work:
                if wrk.done == True:
                    rat_work.append(wrk)
                else:
                    nrat_work.append(wrk)
            return render(request, 'coach/team_homework_work.html', {'team': team, 'work': work, 'rat_work': rat_work, 'nrat_work': nrat_work})
        else:
            return redirect('signin')
    elif request.method == 'POST':
        if request.POST['action'] == 'create':
            try:
                user_pk = int(request.POST['user'])
                h_user = User.objects.filter(pk=user_pk).first()
                comment = request.POST['comment']
                rat = request.POST['select']
                dhw = DoneHomeWork.objects.filter(user=h_user, homework=work).first()
                dhw.rating = int(rat)
                dhw.comment = comment
                dhw.done = True
                dhw.save()
                return redirect('coach_team_homeworks_work',pk, hpk)
            except Exception as e:
                return redirect('coach_team_homeworks_work',pk, hpk)

def team_homeworks_edit(request, pk, hpk):
    if not request.user.is_authenticated and request.user.role == 2:
        return redirect('signin')
    team_l = Team.objects.filter(pk=pk)
    if not team_l.exists():
        return redirect('coach_main')
    team = team_l.first()
    work = HomeWork.objects.filter(pk=hpk).first()

    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            return render(request, 'coach/team_homework_edit.html', {'team': team, 'work': work})
        else:
            return redirect('signin')
    elif request.method == 'POST':
        if request.POST['action'] == 'create':
            try:
                title = request.POST['title']
                text = request.POST['text']
                date = DT.datetime.strptime(request.POST['date'], '%m/%d/%Y') + DT.timedelta(hours=timezone.now().hour, minutes=timezone.now().minute)
                if 'img' in request.FILES:
                    pic = request.FILES.get('img')
                    new = work
                    new.team=team
                    new.name=title
                    new.text=text
                    new.pic=pic
                    new.date=date
                    new.save()
                else:
                    new = work
                    new.team=team
                    new.name=title
                    new.text=text
                    new.date=date
                    new.save()
                return JsonResponse({}, status=200)
            except Exception as e:
                return JsonResponse({'errors': 'Ошибка при редактрировании   ' + e.args[0]}, status=400)

def team_homeworks_create(request, pk):
    if not request.user.is_authenticated and request.user.role == 2:
        return redirect('signin')
    team_l = Team.objects.filter(pk=pk)
    if not team_l.exists():
        return redirect('coach_main')
    team = team_l.first()

    if request.method == 'GET':
        if request.user.is_authenticated and request.user.role == 2:
            return render(request, 'coach/team_homework_create.html', {'team': team})
        else:
            return redirect('signin')
    elif request.method == 'POST':
        if request.POST['action'] == 'create':
            try:
                title = request.POST['title']
                text = request.POST['text']
                date = DT.datetime.strptime(request.POST['date'], '%m/%d/%Y') + DT.timedelta(hours=timezone.now().hour, minutes=timezone.now().minute)
                if 'img' in request.FILES:
                    pic = request.FILES.get('img')
                    new = HomeWork.objects.create(team=team, name=title,text=text, pic=pic, date=date)
                    new.save()
                    for usr in team.users.all():
                        new.not_done.add(usr)
                    new.save()
                else:
                    new = HomeWork.objects.create(team=team, name=title,text=text, date=date)
                    new.save()
                    for usr in team.users.all():
                        new.not_done.add(usr)
                    new.save()
                return JsonResponse({}, status=200)
            except Exception as e:
                return JsonResponse({'errors': 'Ошибка при создании   ' + e.args[0]}, status=400)