from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from recipes.models import Recipe, Tag, Ingredient, Favorite, ShoppingCart
from users.models import Subscription
from .filters import RecipeFilter
from .pagination import CustomPageNumberPagination
from .permissions import IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly
from .serializers import (
    CustomUserCreateSerializer,
    CustomUserSerializer,
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeCreateSerializer,
)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Custom viewset for user operations."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            return CustomUserCreateSerializer
        return CustomUserSerializer

    @action(
        detail=True, methods=["post", "delete"], permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == "POST":
            if user == author:
                return Response(
                    {"error": "Нельзя подписаться на самого себя"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if author.subscribers.filter(user=user).exists():
                return Response(
                    {"error": "Вы уже подписаны на этого пользователя"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            author.subscribers.create(user=user)
            serializer = self.get_serializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            subscription = author.subscribers.filter(user=user)
            if subscription.exists():
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"error": "Вы не подписаны на этого пользователя"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for Tag model."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for Ingredient model."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    search_fields = ("^name",)


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset for Recipe model."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (RecipeFilter,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ("create", "partial_update"):
            return RecipeCreateSerializer
        return RecipeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save(author=self.request.user)
        response_serializer = RecipeSerializer(
            instance=recipe, context={"request": request}
        )
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(
        detail=True, methods=["post", "delete"], permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        return self._handle_recipe_action(request, pk, Favorite, "favorite")

    @action(
        detail=True, methods=["post", "delete"], permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        return self._handle_recipe_action(request, pk, ShoppingCart, "shopping_cart")

    def _handle_recipe_action(self, request, pk, model, action_name):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        obj = model.objects.filter(user=user, recipe=recipe)

        if request.method == "POST":
            if obj.exists():
                return Response(
                    {"error": f"Рецепт уже в {action_name}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            model.objects.create(user=user, recipe=recipe)
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            if obj.exists():
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"error": f"Рецепт не найден в {action_name}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = (
            RecipeIngredient.objects.filter(recipe__shopping_cart__user=user)
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(total_amount=Sum("amount"))
        )

        shopping_list = ["Список покупок:\n"]
        for ingredient in ingredients:
            shopping_list.append(
                f'{ingredient["ingredient__name"]} - '
                f'{ingredient["total_amount"]} '
                f'{ingredient["ingredient__measurement_unit"]}\n'
            )

        response = HttpResponse("".join(shopping_list), content_type="text/plain")
        response["Content-Disposition"] = 'attachment; filename="shopping_list.txt"'
        return response
