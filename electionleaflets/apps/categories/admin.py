from django.contrib     import admin
from categories.models import Category

class CategoryOptions(admin.ModelAdmin):
    list_display         = [ 'name','get_description', 'slug']    
    search_fields        = ['name']  
    ordering             = ['name']
        
    def get_description(self,obj):
        if obj.description:
            return obj.description[0:50]
        return ''
    get_description.short_description = 'Description'

admin.site.register( Category,CategoryOptions )


