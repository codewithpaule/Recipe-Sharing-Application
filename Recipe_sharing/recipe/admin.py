from django.contrib import admin
from .models import Recipe, Step, Ingredient

class StepInline(admin.TabularInline):
    model = Step
    extra = 0  # Set extra to 0 to prevent adding new steps in the admin

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 0  # Set extra to 0 to prevent adding new ingredients in the admin

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [StepInline, IngredientInline]  # Remove StepInline and IngredientInline
    list_display = ('name', 'description', 'tags')
    search_fields = ('name', 'description', 'tags')
    list_filter = ('tags',)
    readonly_fields = ('name', 'description', 'tags', 'image')  # Add readonly_fields to prevent editing existing fields

    def has_add_permission(self, request):
        return False  # Disable the ability to add new recipes from the admin

    def has_change_permission(self, request, obj=None):
        return False  # Disable the ability to change existing recipes from the admin

    # def has_delete_permission(self, request, obj=None):
    #     return False  # Disable the ability to delete existing recipes from the admin

