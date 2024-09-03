from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from recipe.models import Recipe # Import the Recipe model
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from recipe.models import Comment
from .forms import CommentForm
from django.template.loader import render_to_string
from django.http import JsonResponse, Http404
import json

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse


from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages

def send_email(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        email = request.POST.get('email').strip()
        phone = request.POST.get('phone').strip()
        message = request.POST.get('message').strip()

        subject = f"Message from {name.upper()}"

        formatted_message = f"""
        <html>
        <body>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Phone Number:</strong> {phone}</p>
            <p><strong>Message:</strong></p>
            <p>{message}</p>
        </body>
        </html>
        """

        try:
            send_mail(
                subject,
                formatted_message,
                email,  # Sender's email
                ['pauleruvwu@gmail.com'],  # Replace with your email
                fail_silently=False,
                html_message=formatted_message  # Use HTML message
            )
            messages.success(request, "Your message has been sent successfully!")
        except BadHeaderError:
            messages.error(request, "Invalid header found.")
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")

    return render(request, "main/contact.html")


def index(request):
    recipes_list = Recipe.objects.all() 
    paginator = Paginator(recipes_list, 6)  # Paginate recipes, with 6 recipes per page

    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get the recipes for the current page

    return render(request, 'main/index.html', {'page_obj': page_obj})


def recipe(request):
    return render(request, 'main/recipe.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

def faq(request):
    return render(request, 'main/faq.html')

def manage(request):
    return render(request, 'main/manage.html')


def get_replies(comment):
    replies = comment.replies.all()
    replies_data = []
    for reply in replies:
        replies_data.append({
            'id': reply.id,
            'content': reply.content.capitalize(),
            'created_at': reply.created_at.strftime('%B %d, %Y, %I:%M %p'),
            'user': reply.user.get_full_name(),
            'user_initials': f'{reply.user.first_name[0].upper()}{reply.user.last_name[0].upper()}',
            'parent_user': reply.parent.user.get_full_name() if reply.parent else comment.user.get_full_name(),
            'replies': get_replies(reply)  # Recursively get replies of replies
        })
    return replies_data

def recipe_detail_view(request, recipe_name):
    recipe = get_object_or_404(Recipe, name=recipe_name)
    comments = recipe.comments.filter(parent__isnull=True).order_by('-created_at')
    author_recipe_count = Recipe.objects.filter(author=recipe.author).count()
    tags = recipe.tags.split(', ')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent_id')
            parent_comment = None
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
            new_comment = form.save(commit=False)
            new_comment.recipe = recipe
            new_comment.user = request.user
            new_comment.parent = parent_comment
            new_comment.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                response_data = {
                    'success': True,
                    'comment': {
                        'id': new_comment.id,
                        'content': new_comment.content.capitalize(),
                        'created_at': new_comment.created_at.strftime('%B %d, %Y, %I:%M %p'),
                        'user': new_comment.user.get_full_name(),
                        'user_initials': f'{new_comment.user.first_name[0].upper()}{new_comment.user.last_name[0].upper()}',
                        'parent_user': parent_comment.user.get_full_name() if parent_comment else None,
                    },
                }
                return JsonResponse(response_data)
        else:
            form = CommentForm()

    paginator = Paginator(comments, 2)
    comments_page = paginator.page(1)

    context = {
        'recipe': recipe,
        'comments': comments_page,
        'form': CommentForm(),
        'has_more': comments_page.has_next(),
        'recipeCount': author_recipe_count,
        'tags': tags,
    }
    return render(request, 'main/recipe.html', context)

def serialize_comment(comment):
    user_initials = ''.join([name[0].upper() for name in comment.user.username.split() if name])
    return {
        'id': comment.id,
        'user': comment.user.username,
        'user_initials': user_initials,
        'content': comment.content,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'replies': [serialize_comment(reply) for reply in comment.replies.all()],
        'parent_user': comment.parent.user.username if comment.parent else None,
    }

def load_more_comments(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        if not page:
            return JsonResponse({'error': 'Invalid page number'}, status=400)

        try:
            page = int(page)
        except ValueError:
            return JsonResponse({'error': 'Invalid page number'}, status=400)

        recipe_name = request.GET.get('recipe_name')
        if not recipe_name:
            return JsonResponse({'error': 'Recipe not specified'}, status=400)

        recipe = get_object_or_404(Recipe, name=recipe_name)
        comments = recipe.comments.filter(parent=None).order_by('-created_at')
        paginator = Paginator(comments, 5)  # Adjust the number of comments per page as needed

        if page > paginator.num_pages:
            return JsonResponse({'error': 'Page out of range'}, status=400)

        page_comments = paginator.get_page(page)
        comments_list = [serialize_comment(comment) for comment in page_comments]

        return JsonResponse({'comments': comments_list, 'has_more': page < paginator.num_pages}, status=200)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def recipes_by_tag(request, tag):
    recipes_list = Recipe.objects.filter(tags__icontains=tag)
    paginator = Paginator(recipes_list, 6)  # Show 6 recipes per page

    page_number = request.GET.get('page')
    try:
        recipes = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        recipes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        recipes = paginator.page(paginator.num_pages)

    alternative_recipes = Recipe.objects.exclude(tags__icontains=tag)[:6]  # Get alternative recipes

    return render(request, 'main/tags.html', {'recipes': recipes, 'tag': tag, 'alternative_recipes': alternative_recipes})

def search(request):
    query = request.GET.get('query')
    if query:
        recipes = Recipe.objects.filter(name__icontains=query)
        paginator = Paginator(recipes, 6)
        total_results = recipes.count()
        page_number = request.GET.get('page')  # Get the current page number
        page_obj = paginator.get_page(page_number)
    else:
        recipes = []  # Return empty queryset if no query
        total_results = 0

    return render(request, 'main/search-recipes.html', {'recipes': recipes, 'query': query, 'total_results': total_results, 'page_obj': page_obj})


def personal_information(request):
    user = request.user
    return render(request, 'main/manage.html', {'user': user})

def user_shared_recipes(request):
    if request.user.is_authenticated:
        # Retrieve recipes shared by the current user
        shared_recipes = Recipe.objects.filter(author=request.user)
        return render(request, 'main/shared-recipe.html', {'shared_recipes': shared_recipes})
    else:
        # Handle case when user is not logged in
        return render(request, 'main/index.html', {'error_message': 'You must be logged in to view your shared recipes.'})

def delete_recipe(request):
    if request.method == 'GET':
        recipe_id = request.GET.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        # Delete the recipe
        recipe.delete()

        # Provide a JSON response indicating success
        response_data = {'message': 'Recipe deleted successfully'}
        return JsonResponse(response_data)
    
    return JsonResponse({'message': 'Invalid request'}, status=400)

# views.py



