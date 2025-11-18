from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Movie, Review


class TopCommentsViewTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            name='Sample Movie',
            price=10,
            description='Sample description',
            image='movie_images/avatar.jpg'
        )
        self.user_one = User.objects.create_user(username='alice', password='password123')
        self.user_two = User.objects.create_user(username='bob', password='password123')

        self.review_old = Review.objects.create(
            comment='An older comment',
            movie=self.movie,
            user=self.user_one
        )
        self.review_recent = Review.objects.create(
            comment='A newer comment',
            movie=self.movie,
            user=self.user_two
        )

        self.review_old.date = timezone.now() - timezone.timedelta(days=1)
        self.review_old.save(update_fields=['date'])
        self.review_recent.date = timezone.now()
        self.review_recent.save(update_fields=['date'])

    def test_top_comments_orders_reviews_by_most_recent(self):
        response = self.client.get(reverse('movies.top_comments'))

        self.assertEqual(response.status_code, 200)
        top_reviews = list(response.context['template_data']['top_reviews'])
        self.assertEqual(top_reviews, [self.review_recent, self.review_old])

    def test_top_comments_handles_no_reviews(self):
        Review.objects.all().delete()

        response = self.client.get(reverse('movies.top_comments'))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['template_data']['top_reviews'])
