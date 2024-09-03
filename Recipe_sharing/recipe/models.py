from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recipe/recipes/')
    description = models.TextField()
    tags = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Add author field
    def __str__(self):
        return f"{self.name} by {self.author.first_name} {self.author.last_name}"


class Step(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)  # Add this field to store the order

    def __str__(self):
        return f"Step {self.order}"

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)  # Add this field to store the order

    def __str__(self):
        return f"Ingredient {self.order}"

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.name}"
