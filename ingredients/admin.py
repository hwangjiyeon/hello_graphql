from django.contrib import admin

from .models import Category, Ingredient
# Register your models here.

class categoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

class ingredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'notes', 'category')

admin.site.register(Category, categoryAdmin)
admin.site.register(Ingredient, ingredientAdmin)