from logs.models import Log
# from users.forms import CreationForm, LoginForm

def get_mini_posts(request):
    mini_posts = Log.objects.order_by('-date_added')[:5]
    return {'last_5_posts': mini_posts}

# def get_auth_form(request):
#     login_form = LoginForm()
# #     CreateView().form_class = CreationForm
#     signup_form = CreationForm()
#     return {'login_form': login_form, 'signup_form': signup_form}