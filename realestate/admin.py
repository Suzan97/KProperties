from django.contrib import admin
from .models import *
from django import forms

# Register your models here.


class Property_Image(admin.TabularInline):
    model = Property_Image

class Additional_Informations(admin.TabularInline):
    model = Additional_Information

class PropertyAdminForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
        widgets = {
            'Location': forms.TextInput(attrs={'id': 'location-autocomplete'}),
        }

   

class Property_Admin(admin.ModelAdmin):
    search_fields = ['Property_name']
    inlines  = (Property_Image, Additional_Informations)
    list_display = ('Property_name','Price','Category', 'Location')
    list_editable = ('Category', 'Price')
    form = PropertyAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['Location'].widget = forms.TextInput(attrs={'id': 'location-autocomplete'})
        return form

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.property:
            self.fields['name'].initial = self.instance.property.Property_name

class GalleryAdmin(admin.ModelAdmin):
    autocomplete_fields = ['property']
    related_search_fields = {
        'property': ['Property_name'],  # Add more fields if needed
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "property":
            kwargs["queryset"] = Property.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        # Check if the object is being saved for the first time
        if not obj.pk:
            # Populate the 'name' field with the selected Property's Property_name
            obj.name = obj.property.Property_name
        
        super().save_model(request, obj, form, change)
    


admin.site.register(Slider)
admin.site.register(Main_Category)
admin.site.register(Category)
admin.site.register(Property, Property_Admin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Additional_Information)
