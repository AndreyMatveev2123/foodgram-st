from django.contrib import admin
from .models import Ingredient, Tag, Recipe, RecipeIngredient, Favorite, ShoppingCart


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    list_filter = ("author", "name", "tags")
    inlines = [RecipeIngredientInline]
    search_fields = ("name", "author__username")
    readonly_fields = ("favorited_count",)

    def favorited_count(self, obj):
        return obj.favorited_by.count()

    favorited_count.short_description = "Число добавлений в избранное"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "slug")
    search_fields = ("name", "slug")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
