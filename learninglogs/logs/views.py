from django.shortcuts import render
from .models import Log, Group
from django.shortcuts import get_object_or_404, redirect
from .forms import LogForm
from django.contrib.postgres.search import SearchVector


def index(request):
    """The home page for Learning Log."""
    template = 'main.html'
    return render(request, template,)


def groups(request):
    """Show all groups."""
    groups = Group.objects.order_by('title')
    template = 'logs/groups_list.html'
    context = {'groups': groups}
    return render(request, template, context)


def group(request, pk):
    """Show a single group and all its logs."""
    group = get_object_or_404(Group, pk=pk)
    logs = group.logs.order_by('date_added')
    template = 'logs/logs_list.html'
    context = {'group': group, 'logs': logs}
    return render(request, template, context)


def log(request, pk):
    """Show a single log and all its entries."""
    log = get_object_or_404(Log, pk=pk)
    group = Group.objects.filter(logs=log.id).first()
    template = 'logs/log.html'
    context = {'log': log, 'group': group}
    return render(request, template, context)


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


def my_logs(request):
    """Show all logs created by the current user."""
    logs = Log.objects.filter(owner=request.user).order_by('date_added')
    template = 'logs/my_logs.html'
    context = {'logs': logs}
    return render(request, template, context)


def profile_settings(request):
    # показывает страницу настроек профиля
    # можно изменять имя, фамилию, email, пароль
    # можно удалить аккаунт
    # можно добавить аватарку
    # можно добавить о себе
    # можно добавить ссылки на соцсети
    # можно добавить ссылки на другие сайты
    # можно добавить ссылки на другие аккаунты
    
    template = 'logs/profile_settings.html'
    
