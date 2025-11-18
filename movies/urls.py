from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movies.index'),
    path('top-comments/', views.top_comments, name='movies.top_comments'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
    path('petitions/', views.petitions_list, name='movies.petitions_list'),
    path('petitions/create/', views.create_petition, name='movies.create_petition'),
    path('petitions/<int:id>/', views.petition_detail, name='movies.petition_detail'),
    path('petitions/<int:id>/vote/', views.vote_petition, name='movies.vote_petition'),
]