from django.test import TestCase
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from blog.models import BlogPost
from django.utils import timezone


class UserTests(TestCase):
    def test_user_with_permission(self):
        """Checks if a new permission is correctly applied to a new user"""
        content_type = ContentType.objects.get_for_model(BlogPost)
        perm = Permission.objects.create(
            name='Can publish',
            codename='can_publish',
            content_type=content_type
        )

        usr = User.objects.create_user('john', 'john@doe.com', 'johnpswrd000')
        usr.user_permissions.add(perm)
        self.assertEqual(User.objects.filter(user_permissions__codename='can_publish').last(), usr)
        self.assertEqual(User.objects.with_perm(perm).last(), usr)


class BlogPostTests(TestCase):
    def test_blog_creation_date(self):
        """Checks the creation date with different methods"""
        usr = User.objects.create_user('john', 'john@doe.com', 'johnpswrd000')
        blogpost = BlogPost.objects.create(
            title='Save the pandas',
            author=usr,
            txt='''There are just a few pandas in our planet and
            we have to save them because we destroyed their habitat.
            Salven a los rinocerontes tambien, gracias.'''
        )
        pub_date = blogpost.creation_date
        now = timezone.now()
        # they will differ in time (microseconds)
        self.assertEqual(pub_date.date(), now.date())
        self.assertEqual(pub_date.day, now.day)
