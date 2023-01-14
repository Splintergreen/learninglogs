from django.shortcuts import render
from .models import Log, Group
from django.shortcuts import get_object_or_404, redirect
from .forms import LogForm


def index(request):
    """The home page for Learning Log."""
    template = 'index.html'
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
    template = 'logs/create_log.html'
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