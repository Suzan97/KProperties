from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.paginator import UnorderedObjectListWarning

def paginate_queryset(queryset, request, items_per_page):
    paginator = Paginator(queryset.order_by('-date_added'), items_per_page)
    page = request.GET.get('page')
    try:
        queryset_page = paginator.page(page)
    except PageNotAnInteger:
        queryset_page = paginator.page(1)
    except EmptyPage:
        queryset_page = paginator.page(paginator.num_pages)
    return queryset_page

