from django.test import TestCase
from blog.models import BlogPost, Comment
from django.urls import reverse
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType


class BlogViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """ We create a new post cls.blogpost and a new user cls.usr """
        content_type = ContentType.objects.get_for_model(BlogPost)
        perm = Permission.objects.create(
            name='Can publish',
            codename='can_publish',
            content_type=content_type
        )

        cls.usr = User.objects.create_user('john', 'john@doe.com', 'johnpswrd000')
        cls.usr.user_permissions.add(perm)
        cls.blogpost = BlogPost.objects.create(
            author=cls.usr,
            txt='Hello, World!\nThis is my post today\nThank you all for reading it.'
        )

    def test_status_code(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200, 'Page at /blog/ (BlogView)')

    def test_context_returned(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.context['blogs'][0], self.blogpost)
        self.assertEqual(response.context['authors'][0], self.usr)
        self.assertEqual(len(response.context['blogs']), (BlogPost.objects.all()[:3]).count())


class BlogDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """ We create a new post cls.blogpost and a new user cls.usr """
        content_type = ContentType.objects.get_for_model(BlogPost)
        perm = Permission.objects.create(
            name='Can publish',
            codename='can_publish',
            content_type=content_type
        )

        cls.usr = User.objects.create_user('john', 'john@doe.com', 'johnpswrd000')
        cls.usr.user_permissions.add(perm)

        cls.blogpost = BlogPost.objects.create(
            author=cls.usr,
            txt='Hello, World!\nThis is my post today\nThank you all for reading it.'
        )

        cls.comment = Comment.objects.create(blog=cls.blogpost, author=cls.usr, txt='Here is my comment, gimme that Teddy bear')

    def test_response(self):
        url = reverse('blog:blog-detail', args=(self.blogpost.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_context_returned(self):
        url = reverse('blog:blog-detail', args=(self.blogpost.id,))
        response = self.client.get(url)
        self.assertEqual(response.context['comments'].first(), self.blogpost.comment_set.first())


class AuthorDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """ We create a new post cls.blogpost and a new user cls.usr """
        content_type = ContentType.objects.get_for_model(BlogPost)
        perm = Permission.objects.create(
            name='Can publish',
            codename='can_publish',
            content_type=content_type
        )

        cls.usr = User.objects.create_user('john', 'john@doe.com', 'johnpswrd000')
        cls.usr.user_permissions.add(perm)

        cls.blogpost = BlogPost.objects.create(
            author=cls.usr,
            txt='Hello, World!\nThis is my post today\nThank you all for reading it.'
        )

        cls.comment = Comment.objects.create(blog=cls.blogpost, author=cls.usr, txt='Here is my comment, gimme that Teddy bear')

    def test_response(self):
        url = reverse('blog:author-detail', args=(self.usr.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
