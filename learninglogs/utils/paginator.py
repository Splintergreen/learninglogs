from django.core.paginator import Paginator

PAGE_NUM = 2


def page(query, request):
    paginator = Paginator(query, PAGE_NUM)
    page_numer = request.GET.get('page')
    return paginator.get_page(page_numer)
