import json

from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from utils import paginator

from .forms import CommentForm, LogForm, ProfileForm
from .models import Comment, Group, Log, User


def index(request):
    """The home page for Learning Log."""
    # template = 'main.html'
    return redirect('logs:groups_list')


def groups(request):
    """Show all groups."""
    groups = Group.objects.order_by('title')
    page_obj = paginator.page(groups, request)
    template = 'logs/groups_list.html'
    context = {'page_obj': page_obj}
    return render(request, template, context)


def group(request, pk):
    """Show a single group and all its logs."""
    group = get_object_or_404(Group, pk=pk)
    logs = Log.objects.filter(group=group.id)
    page_obj = paginator.page(logs, request)
    template = 'logs/logs_list.html'
    context = {'group': group, 'page_obj': page_obj}
    return render(request, template, context)


def log(request, pk):
    """Show a single log and all its entries."""
    log = get_object_or_404(Log, pk=pk)
    group = Group.objects.filter(log=log.id)
    comments = Comment.objects.filter(log_id=log.pk)
    form = CommentForm(request.POST or None)
    template = 'logs/log.html'
    is_liked = False
    if log.likes.filter(id=request.user.id).exists():
        is_liked = True

    context = {
        'log': log,
        'group': group,
        'form': form,
        'comments': comments,
        'is_liked': is_liked,
    }
    return render(request, template, context)


def like(request):
    """Like a log."""
    data = json.loads(request.body)
    log = get_object_or_404(Log, pk=data["id"])
    checker = None
    if request.user.is_authenticated:
        if log.likes.filter(id=request.user.id).exists():
            log.likes.remove(request.user)
            checker = 0
        else:
            log.likes.add(request.user)
            checker = 1
    likes = log.likes.count()
    info = {
        "check": checker,
        "num_of_likes": likes,
    }
    return JsonResponse(info, safe=False)


@login_required
def create_log(request):
    """Create a new log."""
    template = 'logs/create_or_edit_log.html'
    form = LogForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        new_log = form.save(commit=False)
        new_log.owner = request.user
        new_log.save()
        return redirect('logs:log', pk=new_log.pk)
    context = {'form': form}
    return render(request, template, context)


@login_required
def edit_log(request, pk):
    """Edit an existing log."""
    log = get_object_or_404(Log, pk=pk)
    template = 'logs/create_or_edit_log.html'
    form = LogForm(
        request.POST or None, files=request.FILES or None, instance=log
    )
    if log.owner != request.user:
        return redirect('logs:index')
    if form.is_valid():
        form.save()
        return redirect('logs:log', pk=log.pk)
    context = {'log': log, 'form': form, 'is_edit': True, }
    return render(request, template, context)


def search(request):
    """Search for logs."""
    template = 'logs/search.html'
    query = request.GET.get('search_query')
    results = Log.objects.annotate(
        search=SearchVector('text', 'description'),
        ).filter(search=query)
    context = {'results': results}
    return render(request, template, context)


@login_required
def my_logs(request):
    """Show all logs created by the current user."""
    logs = Log.objects.filter(owner=request.user).order_by('date_added')
    page_obj = paginator.page(logs, request)
    template = 'logs/my_logs.html'
    context = {'page_obj': page_obj}
    return render(request, template, context)


def user_logs(request, username):
    """Show all logs created by the current user."""
    user = get_object_or_404(User, username=username)
    logs = Log.objects.filter(owner_id=user.id).order_by('date_added')
    page_obj = paginator.page(logs, request)
    template = 'logs/my_logs.html'
    context = {'page_obj': page_obj}
    return render(request, template, context)


@login_required
def profile_settings(request):
    """Edit an existing log."""
    user = get_object_or_404(User, id=request.user.id)
    template = 'logs/profile_settings.html'
    form = ProfileForm(
        request.POST or None, files=request.FILES or None, instance=user
    )
    if user.is_anonymous:
        return redirect('logs:index')
    if form.is_valid():
        form.save()
        return redirect('logs:profile_settings')
    context = {'user': user, 'form': form, }
    return render(request, template, context)


@login_required
def add_comment(request, pk):
    log = get_object_or_404(Log, pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.log = log
        comment.save()
    return redirect('logs:log', pk=pk)


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    print('delete')
    if request.user == comment.author:
        comment.delete()
    return redirect('logs:log', pk=comment.log.pk)


def favorite_logs(request):
    """Show liked logs for the current user."""
    user = request.user
    logs = user.likes.all()
    page_obj = paginator.page(logs, request)
    template = 'logs/my_logs.html'
    context = {'page_obj': page_obj}
    return render(request, template, context)
