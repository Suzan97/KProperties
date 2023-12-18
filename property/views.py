from django.shortcuts import redirect,render, get_object_or_404
from realestate.models import Slider, Main_Category, Property, Additional_Information, Property_Image, Gallery, Category
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.paginator import Paginator
from realestate.utils import paginate_queryset
from django.db.models import F
from django.db.models import Q
from .forms import PropertySearch
from django.utils import timezone
from urllib.parse import unquote,quote
from django.http import Http404


def BASE(request):
    return render(request, 'base.html')
    
def handler404(request, exception):
    return render(request, 'Error_404.html', status=404)

def HOME(request):
    slider = Slider.objects.all().order_by('-id')[0:3]
    property = Property.objects.all().order_by('-date_added')[:4]
    pop_property = Property.objects.all().order_by('-page_visits')[:4]
    main_cat = Main_Category.objects.all().distinct('name')
    sub_cat = Category.objects.all().distinct('name')
    latest = Property.objects.order_by('-date_added')[:4]
    

    context = {'slider': slider, 'property': property,'pop_property':pop_property, 'main_cat':main_cat, 'sub_cat':sub_cat,
               'latest':latest}
    return render(request, 'Main/index.html', context)

def PROP(request):
    property = Property.objects.all().order_by('-date_added')
    items_per_page = 10
    pop_property = Property.objects.order_by('-page_visits')[:3]
    sub_cat = Category.objects.all().distinct('name')

    categories = set(property.Category.name for property in property)

    property_page = paginate_queryset(property, request, items_per_page)

    context = {'property': property_page, 'pop_property':pop_property, 'categories':categories, 'sub_cat':sub_cat}
    return render(request, 'Main/property.html', context)


def get_current_datetime(request):
    current_datetime = timezone.now()

def PROP_DETAIL(request,slug):
    property = get_object_or_404(Property, slug = slug)
    sub_cat = Category.objects.all().distinct('name')
    property.page_visits +=1
    property.save()

    location_url = property.location_url 

    tags_list = [tag.strip().lower() for tag in property.Tags.split(',') if tag.strip()]

    # Construct a Q object for each tag in tags_list
    tag_queries = [Q(Tags__icontains=tag) for tag in tags_list]

    # Combine the Q objects with OR conditions
    combined_tags_query = Q()
    for tag_query in tag_queries:
        combined_tags_query |= tag_query

    same_prop = Property.objects.filter(
        combined_tags_query
    ).exclude(id=property.id).distinct()[:3]

      # Construct a Q object for each word in the current property's location
    location_words = property.Location.split()
    location_queries = [Q(Location__icontains=word) for word in location_words]

    # Combine the Q objects with OR conditions
    combined_location_query = Q()
    for location_query in location_queries:
        combined_location_query |= location_query

    pop_property =  Property.objects.order_by('-page_visits')[:3]
    nearby_prop = Property.objects.filter(
        combined_location_query
    ).exclude(id=property.id).distinct()[:3]
    
    image = Property_Image.objects.filter(property=property)
    add_info = Additional_Information.objects.filter(property=property)
    print('nearby location:', nearby_prop)


    context = {'property': property,'sub_cat':sub_cat , 'location_url': location_url, 'same_prop':same_prop,
                'image':image, 'add_info': add_info, 'nearby_prop': nearby_prop, 'pop_property': pop_property }
    return render(request, 'Main/property_detail.html', context)

def get_main_category_name_dynamically(name):
    # Your logic to determine the main category dynamically
    # For simplicity, let's assume it returns a Main_Category instance
    decoded_name = unquote(name)
    try:
        # Use get() with an exception for DoesNotExist
        return Main_Category.objects.get(name=decoded_name)
    except Main_Category.DoesNotExist:
        raise Http404("Currently unavailable")


def CAT_DETAIL(request, category):
    decoded_category = unquote(category)
    main_category_instance = get_main_category_name_dynamically(decoded_category)
    property = Property.objects.filter(Category__main_category__name=main_category_instance.name)
    property_main = Property.objects.filter(Category__main_category=main_category_instance)
    pop_property = Property.objects.order_by('-page_visits')[:3]
    
    if main_category_instance is None:
        # Handle the case where the category doesn't exist
        context = {'error': 'Category currently not available'}
        return render(request, 'Error_404.html', context)

    categories = set(property.Category.name for property in property)
    sub_cat = Category.objects.all().distinct('name')

    items_per_page = 10
    property_page = paginate_queryset(property, request, items_per_page)

    print("property_page length:", len(property_page))
    context = {'category': decoded_category, 'main_category_instance': main_category_instance,'property':property_page, 'property_main':property_main,
               'pop_property': pop_property, 'categories':categories, 'sub_cat':sub_cat}
    return render(request, 'Main/category.html', context)

def PROP_CATEGORY(request, category,main_category=None):
    decoded_category = unquote(category)
    decoded_main_category = None # Initialize the variable

    if main_category:
        decoded_main_category = unquote(main_category)
        property = Property.objects.filter(
            Category__main_category__name=decoded_main_category,
            Category__name=decoded_category
        )
    else:
        # If main_category is not provided, only filter by category
        property = Property.objects.filter(Category__name=decoded_category)

    pop_property = Property.objects.order_by('-page_visits')[:3]
    sub_cat = Category.objects.all().distinct('name')

    items_per_page = 10
    property_page = paginate_queryset(property, request, items_per_page)
    categories = set(property.Category.name for property in property)

    if not property.exists():  # Check if the queryset is empty
        print(f"No properties found for category: {decoded_category}")
        return render(request, 'Main/Error_404.html', {'error_message': 'No properties currently available for this category.'})

    context = {'property': property_page, 'pop_property': pop_property, 'sub_cat': sub_cat, 'category': decoded_category, 'main_category': decoded_main_category, 'categories': categories}
    return render(request, 'Main/property_category.html', context)

def PROP_LATEST(request):
    property = Property.objects.all()
    latest_prop = Property.objects.order_by('-date_added')
    pop_property = Property.objects.order_by('-page_visits')[:3]
    
    categories = set(property.Category.name for property in property)


    items_per_page = 6
    property_page = paginate_queryset(latest_prop, request, items_per_page)

    context = {'property':property, 'property':property_page, 'latest_prop':latest_prop, 'categories':categories }

    return render(request,  'Main/property_latest.html', context)  

def PROP_POPULAR(request):
    property = Property.objects.all()
    popular = Property.objects.all().order_by('-page_visits')[:4]
    pop_property = Property.objects.order_by('-page_visits')[:3]

    categories = set(property.Category.name for property in property)


    items_per_page = 6
    property_page = paginate_queryset(property, request, items_per_page)

    context = {'property':property, 'property':property_page, 'popular':popular , 'pop_property':pop_property,
                'categories':categories }

    return render(request,  'Main/property_popular.html', context)  

def GALLERY(request):
    gallery = Gallery.objects.all()
    category = Category.objects.all().distinct('name')


    context = {'gallery': gallery, 'category':category}

    return render(request, 'Main/gallery.html', context)

def PROP_SEARCH(request):
    property = Property.objects.all()
    pop_property =  Property.objects.order_by('-page_visits')[:3]
    sub_cat = Category.objects.all().distinct('name')
    location = request.GET.get('location', '')
    name = request.GET.get('name', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    query_params = {}

    if location:
        query_params['Location__icontains'] = location
    if name:
        query_params['Property_name__icontains'] = name
    if category:
        query_params['Category__id'] = category
    if min_price:
        query_params['Price__gte'] = min_price
    if max_price:
        query_params['Price__lte'] = max_price

    property = property.filter(**query_params)

    categories = set(property.Category.name for property in property)


    context = {'property': property, 'pop_property':pop_property, 'location': location, 'name': name,
                'category': category, 'sub_cat':sub_cat, 'categories':categories}
    return render(request, 'Main/search_results.html', context)


def CONTACT(request):   
    return render(request, 'Main/contact.html')