from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save
import datetime 
from django.utils import timezone
from datetime import datetime
# Create your models here.

CURRENCY_CHOICES = (
        ('USD' , 'USD'),
        ('KES', 'KES'),
    )
class Slider(models.Model):

    Image = models.ImageField(upload_to='slider_imgs')
    Property_name = models.CharField(max_length=200)
    size = models.CharField(max_length=200, null = True)
    Location = models.CharField(max_length=200, null=True)
    Discount = models.IntegerField(blank=True, null=True)
    Currency = models.CharField(choices=CURRENCY_CHOICES, max_length=4,null=True,blank=True)
    Price = models.CharField(max_length=100, null=True)
    Link = models.CharField(max_length=200)

    def __str__(self):
        return self.Property_name

class Main_Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    main_category = models.ForeignKey(Main_Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " -- " + self.main_category.name
    

def get_current_datetime():
	return timezone.now()


class Property(models.Model):

    Property_name = models.CharField(max_length=200)
    Short_description = RichTextField(null=True)
    Description = RichTextField()
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Property_image = models.ImageField(upload_to='media/property_img')
    Property_video = models.FileField(upload_to='media/property_img',null= True, blank=True)
    Location = models.CharField(max_length=200)
    location_url = models.CharField(max_length=500, null=True, blank=True)
    Currency = models.CharField(choices=CURRENCY_CHOICES, max_length=4,null=True,blank=True)
    Price = models.CharField(max_length=100, null=True)
    slug = models.SlugField(default='', max_length=500,null=True, blank=True)
    Tags = models.CharField(max_length=100, null=True)
    page_visits = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(default=get_current_datetime)
    

    def __str__(self):
        return self.Property_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("property_detail", kwargs={'slug': self.slug})

def create_slug(instance, new_slug=None):
    slug = slugify(instance.Property_name)
    if new_slug is not None:
        slug = new_slug
    qs = Property.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Property)

class Property_Image(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    Image_url = models.CharField(max_length=200)

class Additional_Information(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    features = models.CharField(max_length =100)
    

class Gallery(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='galleries')
    Image = models.ImageField(upload_to='media/gallery')
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(default='', max_length=500,null=True, blank=True)
    

    def __str__(self):
        return self.name
    
def create_gallery_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Property.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_gallery_slug(instance, new_slug=new_slug)
    return slug

def pre_save_gallery_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_gallery_slug(instance)
    print("Signal handler for Gallery is called.")

pre_save.connect(pre_save_gallery_receiver, sender=Gallery)


    

     