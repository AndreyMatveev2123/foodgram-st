from django_filters import rest_framework as filters
from recipes.models import Recipe, Tag


class RecipeFilter(filters.FilterSet):
    """
    Custom filter set for Recipe model.
    """

    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )
    is_favorited = filters.BooleanFilter(method="filter_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(method="filter_is_in_shopping_cart")
    author = filters.NumberFilter(field_name="author__id")

    class Meta:
        model = Recipe
        fields = ["tags", "author", "is_favorited", "is_in_shopping_cart"]

    def filter_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorited_by__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(in_shopping_cart__user=self.request.user)
        return queryset
