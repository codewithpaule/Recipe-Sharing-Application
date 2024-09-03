from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('', index, name='home'),
    path('recipe/', recipe, name='recipe'),
    path('contact/', contact, name='contact'),
    path('send_email/', send_email, name='send_email'),
    path('about/', about, name='about'),
    path('faq/', faq, name='faq'),
    path('manage/', manage, name='manage'),
    path('recipes/<str:recipe_name>/', recipe_detail_view, name='recipe_detail'),
    path('load-more-comments/', load_more_comments, name='load_more_comments'),
    path('recipes/tag/<str:tag>/', recipes_by_tag, name='recipes_by_tag'),
    path('personal-information/', personal_information, name='personal-information'),
    path('search/', search, name='search'),
    path('delete_recipe/', delete_recipe, name='delete_recipe'),
    path('shared-recipes/', user_shared_recipes, name='shared-recipes'),
]

# Add the following line at the end to serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)