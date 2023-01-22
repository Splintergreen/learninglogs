from django.shortcuts import render
from .models import Log, Group, User, Comment
from django.shortcuts import get_object_or_404, redirect
from .forms import LogForm, ProfileForm, CommentForm
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required
from utils import paginator


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
    logs = group.logs.order_by('date_added')
    page_obj = paginator.page(logs, request)
    template = 'logs/logs_list.html'
    context = {'group': group, 'page_obj': page_obj}
    return render(request, template, context)


def log(request, pk):
    """Show a single log and all its entries."""
    log = get_object_or_404(Log, pk=pk)
    group = Group.objects.filter(logs=log.id).first()
    comments = Comment.objects.filter(log_id=log.pk)
    form = CommentForm(request.POST or None)
    template = 'logs/log.html'
    context = {'log': log, 'group': group, 'form': form, 'comments': comments}
    return render(request, template, context)


@login_required
def create_log(request):
    """Create a new log."""
    template = 'logs/create_or_edit_log.html'
    form = LogForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        new_log = form.save(commit=False)
        new_log.owner = request.user
        new_log.save()
        Group.logs.through.objects.create(
            log=new_log, group_id=request.POST.get('group')
        )
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
    user = request.user
    template = 'logs/profile_settings.html'
    form = ProfileForm(
        request.POST or None, files=request.FILES or None, instance=user
    )
    if user.is_anonymous:
        return redirect('logs:index')
    if form.is_valid():
        form.save()
        return redirect('logs:my_logs')
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
