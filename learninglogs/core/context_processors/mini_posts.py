from logs.models import Log


def get_mini_posts(request):
    mini_posts = Log.objects.order_by('-date_added')[:5]
    return {'last_5_posts': mini_posts}
