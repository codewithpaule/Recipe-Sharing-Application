from django.shortcuts import render, redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def share(request):
    if request.method == 'POST':
        name = request.POST.get('recipeName')
        description = request.POST.get('recipeDescription')
        tags = request.POST.getlist('recipeTags')
        image = request.FILES.get('profilePicture')

        recipe = Recipe.objects.create(
            name=name,
            description=description,
            tags=', '.join(tags),
            image=image,
            author=request.user
        )

         # Extract and save steps
        step_descriptions = [request.POST[key] for key in request.POST.keys() if key.startswith('recipeProcedure')]
        for order, description in enumerate(step_descriptions, start=1):
            Step.objects.create(recipe=recipe, description=description, order=order)

        # Extract and save ingredients
        ingredient_names = [request.POST[key] for key in request.POST.keys() if key.startswith('recipeIngredient')]
        for order, name in enumerate(ingredient_names, start=1):
            Ingredient.objects.create(recipe=recipe, name=name, order=order)

        return redirect('home')
    else:
        recipes = Recipe.objects.all()
        return render(request, 'recipe/share.html', {'recipes': recipes})
