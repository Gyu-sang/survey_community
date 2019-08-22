from django.shortcuts import render, get_object_or_404
from .models import Post, Withdraw, Deposit, Comment2
from .forms import PostForm, WithdrawForm, DepositForm, CommentForm2
from accounts.models import Profile
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.utils import timezone
# Create your views here.


def survey_list(request):
    page = request.GET.get('page', '1')
    if page == "":
        page = '1'
    page = int(page)
    post_list = Post.objects.all().order_by('-notice', 'finish', '-finished_at', '-pk')
    num = 10
    paginator = Paginator(post_list, num)
    is_paginated = True if paginator.num_pages > 1 else False
    post_list = paginator.page(page)
    page_numbers_range = 5
    start_index = 1
    max_index = len(paginator.page_range)
    for i in reversed(range(1,page+1)):
        if i% page_numbers_range == 1:
            start_index = i
            break
    end_index = start_index + page_numbers_range

    if end_index > max_index:
        end_index = max_index
        page_range = range(start_index, end_index+1)
    else:
        page_range = range(start_index, end_index)



    return render(request, 'survey/survey_list.html', {
        'post_list':post_list,
        'page_range':page_range,
        'is_paginated':is_paginated,
    })

@login_required
def survey_detail(request, pk):
    page = request.GET.get('page', '1')
    if page == "":
        page = '1'
    page = int(page)
    post_list = Post.objects.all().order_by('finish', '-finished_at', '-pk')
    num = 10
    paginator = Paginator(post_list, num)

    is_paginated = True if paginator.num_pages > 1 else False
    post_list = paginator.page(page)

    page_numbers_range = 5
    start_index = 1
    max_index = len(paginator.page_range)

    for i in reversed(range(1,page+1)):
        if i% page_numbers_range == 1:
            start_index = i
            break
    end_index = start_index + page_numbers_range

    if end_index > max_index:
        end_index = max_index
        page_range = range(start_index, end_index+1)
    else:
        page_range = range(start_index, end_index)

    post = Post.objects.get(pk=pk)
    user = User.objects.get(id=request.user.id)
    comment_list = post.comment2_set.filter(author=user)

    # 자동 크레딧 환급 기능
    # profile = Profile.objects.filter(user=user).get()

    if post.finish == False:
        if post.finished_at <= timezone.now():
            post.finish = True
            # 자동 크레딧 환급 기능
            # profile.credit += post.credit * post.participant
            # profile.save()
            post.save()
    return render(request, 'survey/survey_detail.html', {
        'post':post,
        'post_list':post_list,
        'comment_list':comment_list,
        'page_range':page_range,
        'is_paginated':is_paginated,    })

@login_required
def survey_new(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.filter(user=user).get()
        form = PostForm(request.POST)
        total = int(form.data['credit']) * int(form.data['max_participant'])

        if profile.credit > total:
            if form.is_valid():
                profile.credit -= total
                profile.question += 1
                profile.save()
                post = form.save(commit=False)
                post.author = request.user
                post.participant = post.max_participant
                post.save()
                # form.data['participant'] = int(form.data['max_participant'])
                return redirect('survey:survey_list')
        else :
            form = PostForm()
    else:
        form = PostForm()
    return render(request, 'survey/survey_new.html', {
        'form':form,
    })



@login_required
def post_delete(request, pk):
    if request.method =="POST":
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.filter(user=user).get()
        post = Post.objects.get(pk=pk)
        post.delete()
        profile.credit += post.credit * post.participant
        profile.save()
        return redirect('survey:survey_list')

@login_required
def comment_delete(request, pk, pk2):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.filter(user=user).get()
        post = Post.objects.get(pk=pk)
        comment = post.comment2_set.filter(pk=pk2)
        comment.delete()
        profile.credit -= post.credit
        profile.answer -= 1
        profile.save()
        post.participant += 1
        post.save()
        return redirect('survey:survey_detail', pk=pk)

@login_required
def comment_edit(request, pk, pk2):
    post = Post.objects.get(pk=pk)
    post_list = Post.objects.all()
    user = User.objects.get(id=request.user.id)

    comment_list = post.comment2_set.filter(author=user)
    if len(comment_list) != 0:
        comment = Comment2.objects.get(pk=pk2)
    else:
        return redirect('survey:comment_new2', pk=pk)

    form = CommentForm2(request.POST or None, request.FILES, instance=comment)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('survey:survey_detail', pk=pk)

    return render(request, 'survey/comment_edit.html', {
        'form':form,
        'post':post,
    })

@login_required
def calculate(request):
    user = User.objects.get(id=request.user.id)
    withdraw = Withdraw.objects.filter(author=user)
    deposit = Deposit.objects.filter(author=user)
    total_withdraw = 0
    for i in withdraw:
        total_withdraw += i.credit_wait
    total_deposit = 0
    for j in deposit:
        total_deposit += j.credit_wait

    return render(request, 'survey/calculate_list.html',{
        'total_withdraw':total_withdraw,
        'total_deposit':total_deposit,
    })

@login_required
def withdraw(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.filter(user=user).get()
        form = WithdrawForm(request.POST)
        if profile.credit > int(form.data['credit']):
            if form.is_valid():
                withdraw = form.save(commit=False)
                withdraw.author = request.user
                withdraw.done = False
                withdraw.credit_wait = withdraw.credit
                withdraw.save()

                return redirect('survey:calculate')
            else:
                form = WithdrawForm(request.POST)
    else :
        form =WithdrawForm()
    return render(request, 'survey/calculate_withdraw.html', {
        'form':form,
    })

@login_required
def deposit(request):
    if request.method == "POST":
        form = DepositForm(request.POST)

        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.author = request.user
            deposit.done = False
            deposit.credit_wait = deposit.credit
            deposit.save()

            return redirect('survey:calculate')
    else :
        form =DepositForm()
    return render(request, 'survey/calculate_deposit.html', {
        'form':form,
    })


@login_required
def comment_new2(request, pk):
    post = Post.objects.get(pk=pk)
    post_list = Post.objects.all()
    user = User.objects.get(id=request.user.id)

    comment_list = post.comment2_set.filter(author=user)
    if len(comment_list) != 0:
        return render(request, 'survey/comment_error.html', {
            'post':post,
        })
    elif post.finish == True:
        return render(request, 'survey/comment_error2.html', {
            'post':post,
        })


    elif (request.method == "POST") & len(comment_list)==0:
        form = CommentForm2(request.POST, request.FILES)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = get_object_or_404(Post, pk=pk)
            comment.author = request.user
            comment.done = True
            comment.save()

            profile = Profile.objects.filter(user=user).get()

            profile.credit += post.credit
            profile.answer += 1
            post.participant -= 1
            if post.participant == 0:
                post.finish = True
            post.save()
            profile.save()

            return redirect('survey:survey_detail', pk=pk)

    else:
        form = CommentForm2()
    return render(request, 'survey/comment_new2.html', {
        'form':form,
        'post':post,
    })

@login_required
def update(request):
    post_list = Post.objects.filter(finish=False)
    for post in post_list:
        if post.finished_at <= timezone.now():
            post.finish = True

            post.save()
    return render(request, 'survey/update.html')

@login_required
def my_survey(request):
    page = request.GET.get('page', '1')
    if page == "":
        page = '1'
    page = int(page)

    user = User.objects.get(id=request.user.id)
    post_list = Post.objects.filter(author=user).order_by('-pk')

    num = 10
    paginator = Paginator(post_list, num)
    is_paginated = True if paginator.num_pages > 1 else False
    post_list = paginator.page(page)
    page_numbers_range = 5
    start_index = 1
    max_index = len(paginator.page_range)
    for i in reversed(range(1,page+1)):
        if i% page_numbers_range == 1:
            start_index = i
            break
    end_index = start_index + page_numbers_range

    if end_index > max_index:
        end_index = max_index
        page_range = range(start_index, end_index+1)
    else:
        page_range = range(start_index, end_index)

    return render(request, 'survey/my_survey.html' , {
        'post_list':post_list,
        'page_range':page_range,
        'is_paginated':is_paginated,
    })

@login_required
def my_comment(request):
    page = request.GET.get('page', '1')
    if page == "":
        page = '1'
    page = int(page)
    user = User.objects.get(id=request.user.id)
    comment_list = Comment2.objects.filter(author=user).order_by('-pk')

    num = 10
    paginator = Paginator(comment_list, num)
    is_paginated = True if paginator.num_pages > 1 else False
    comment_list = paginator.page(page)
    page_numbers_range = 5
    start_index = 1
    max_index = len(paginator.page_range)

    for i in reversed(range(1,page+1)):
        if i% page_numbers_range == 1:
            start_index = i
            break
    end_index = start_index + page_numbers_range

    if end_index > max_index:
        end_index = max_index
        page_range = range(start_index, end_index+1)
    else:
        page_range = range(start_index, end_index)

    return render(request, 'survey/my_comment.html', {
        'comment_list':comment_list,
        'page_range':page_range,
        'is_paginated':is_paginated,
    })
