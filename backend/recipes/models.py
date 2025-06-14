from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

MAX_AMOUNT = 32000

class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название ингредиента")
    measurement_unit = models.CharField(max_length=50, verbose_name="Единица измерения")

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ['name']
        unique_together = ('name', 'measurement_unit')

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"

class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name="Название тега")
    color = models.CharField(max_length=7, unique=True, verbose_name="HEX-код")
    slug = models.SlugField(max_length=32, unique=True, verbose_name="Слаг")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']

    def __str__(self):
        return self.name

class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipes", verbose_name="Автор рецепта"
    )
    name = models.CharField(max_length=200, verbose_name="Название рецепта")
    image = models.ImageField(upload_to="recipes/images/", verbose_name="Фото блюда")
    text = models.TextField(verbose_name="Описание")
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name="Ингредиенты"
    )
    tags = models.ManyToManyField(
        Tag, related_name="recipes", verbose_name="Теги"
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления (мин)",
        validators=[MinValueValidator(1), MaxValueValidator(MAX_AMOUNT)]
    )
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Ингредиент")
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        validators=[MinValueValidator(1), MaxValueValidator(MAX_AMOUNT)]
    )

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"
        unique_together = ('recipe', 'ingredient')
        ordering = ['id']

    def __str__(self):
        return f"{self.ingredient.name} для {self.recipe.name}"

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites", verbose_name="Пользователь")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="favorited_by", verbose_name="Рецепт")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        unique_together = ('user', 'recipe')
        ordering = ['id']

    def __str__(self):
        return f"{self.user} -> {self.recipe}"

class ShoppingCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shopping_cart", verbose_name="Пользователь")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="in_shopping_cart", verbose_name="Рецепт")

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        unique_together = ('user', 'recipe')
        ordering = ['id']

    def __str__(self):
        return f"{self.user} покупает {self.recipe}" 