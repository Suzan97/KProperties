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

def BASE(request):
    return render(request, 'base.html')

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
    property = Property.objects.all().order_by('id')
    items_per_page = 10
    pop_property = Property.objects.order_by('-page_visits')[:3]
    sub_cat = Category.objects.all().distinct('name')

    categories = set(property.Category.name for property in property)

    property_page = paginate_queryset(property, request, items_per_page)

    context = {'property': property_page, 'pop_property':pop_property, 'categories':categories, 'sub_cat':sub_cat}
    return render(request, 'Main/property.html', context)

def get_main_category_name_dynamically(name):
    # Your logic to determine the main category dynamically
    # For simplicity, let's assume it returns a Main_Category instance
    return Main_Category.objects.get(name=name)


def CAT_DETAIL(request, category):
    main_category_instance = get_main_category_name_dynamically(category)
    property = Property.objects.filter(Category__main_category__name=main_category_instance.name)
    property_main = Property.objects.filter(Category__main_category=main_category_instance)
    pop_property = Property.objects.order_by('-page_visits')[:3]

    categories = set(property.Category.name for property in property)
    sub_cat = Category.objects.all().distinct('name')

    items_per_page = 10
    property_page = paginate_queryset(property, request, items_per_page)

    print("property_page length:", len(property_page))
    context = {'category': category, 'main_category_instance': main_category_instance,'property':property_page, 'property_main':property_main,
               'pop_property': pop_property, 'categories':categories, 'sub_cat':sub_cat}
    return render(request, 'Main/category.html', context)


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

def PROP_CATEGORY(request,category):
    property = Property.objects.filter(Category__name=category)
    pop_property = Property.objects.order_by('-page_visits')[:3]
    sub_cat = Category.objects.all().distinct('name')
    # Use the main category in the query
    # main_category_instance = get_main_category_name_dynamically(category)
    # property_main = Property.objects.filter(Category__main_category=main_category_instance)

    items_per_page = 10
    property_page = paginate_queryset(property, request, items_per_page)
    # display categories in dropdown
    categories = set(property.Category.name for property in property)

    context = {'property':property_page, 'pop_property':pop_property, 'sub_cat':sub_cat, 'category': category, 'categories':categories}
    return render(request, 'Main/property_category.html', context)

def PROP_DETAIL(request,slug):
    property = get_object_or_404(Property, slug = slug)
    sub_cat = Category.objects.all().distinct('name')
    property.page_visits +=1
    property.save()

    location_url = property.location_url

    #similar property and order by date in descending order
    same_category = Property.objects.filter(Category=property.Category).exclude(id=property.id)
    same_prop = same_category.order_by('-date_added')[:3]
    aware_date_added = property.date_added.astimezone(timezone.utc)
    similar = Property.objects.filter(
        Category = property.Category,
        date_added__lt=aware_date_added
    ).exclude(id=property.id).order_by('-date_added')[:3]
    print("Same category properties:", same_category)
    print("More like this properties:", same_prop)
    print("Aware date_added:", aware_date_added)


    pop_property =  Property.objects.order_by('-page_visits')[:3]
    nearby_prop = Property.objects.filter(Location=property.Location).exclude(id=property.id)
    image = Property_Image.objects.filter(property=property)
    add_info = Additional_Information.objects.filter(property=property)

    context = {'property': property,'sub_cat':sub_cat , 'same_prop':same_prop, 'location_url': location_url, 'image':image, 'add_info': add_info, 'nearby_prop': nearby_prop,
               'pop_property': pop_property }
    return render(request, 'Main/property_detail.html', context)

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