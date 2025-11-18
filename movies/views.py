from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Petition
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def top_comments(request):
    top_reviews = Review.objects.select_related('movie', 'user').order_by('-date')

    template_data = {}
    template_data['title'] = 'Top Comments'
    template_data['top_reviews'] = top_reviews
    return render(request, 'movies/top_comments.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)

    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

def petitions_list(request):
    petitions = Petition.objects.all().order_by('-created_at')
    template_data = {}
    template_data['title'] = 'Movie Petitions'
    template_data['petitions'] = petitions
    return render(request, 'movies/petitions.html', {'template_data': template_data})

@login_required
def create_petition(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        if title and description:
            petition = Petition(title=title, description=description, submitted_by=request.user)
            petition.save()
            messages.success(request, 'Petition created successfully!')
            return redirect('movies.petitions_list')
        else:
            messages.error(request, 'Please fill in both title and description.')
    return render(request, 'movies/create_petition.html')

def petition_detail(request, id):
    petition = get_object_or_404(Petition, id=id)
    template_data = {}
    template_data['title'] = petition.title
    template_data['petition'] = petition
    return render(request, 'movies/petition_detail.html', {'template_data': template_data})

@login_required
def vote_petition(request, id):
    petition = get_object_or_404(Petition, id=id)
    if request.user in petition.votes.all():
        petition.votes.remove(request.user)
    else:
        petition.votes.add(request.user)
    return redirect('movies.petition_detail', id=id)