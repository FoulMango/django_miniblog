from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views import View, generic

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import BlogPost, Comment
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm


class MainPage(View):
    @staticmethod
    def get(request):
        return render(request, 'blog/base_generic.html')


class BlogView(View):
    @staticmethod
    def get(request):
        q = BlogPost.objects.all()
        context = {
            'blogs': q[:3],
            'authors': [blog.author for blog in q[:3]]
        }
        return render(request, 'blog/blog_template.html', context=context)


class BlogListView(generic.ListView):
    model = BlogPost
    context_object_name = 'blogs'
    paginate_by = 5


class BlogDetailView(generic.DetailView):
    model = BlogPost
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = context['blog'].id
        context['comments'] = BlogPost.objects.get(pk=pk).comment_set.all()  # Evitando hacer la consulta en la plantilla
        return context


class AuthorDetailView(generic.DetailView):
    model = User
    context_object_name = 'author'
    template_name = 'blog/author_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = context['author'].id
        usr = User.objects.get(pk=pk)
        context['blogs'] = usr.blogpost_set.all()
        try:
            context['bio'] = usr.biography.bio
        except User.biography.RelatedObjectDoesNotExist:
            pass
        return context


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)


@login_required
def add_comment_view(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            Comment.objects.create(
                author=request.user,
                blog=BlogPost.objects.get(id=pk),
                txt=form.cleaned_data['comment']
            )
            return HttpResponseRedirect(reverse('blog:blog-detail', args=(pk,)))
    else:
        form = CommentForm

    return render(request, 'blog/create_comment.html', context={'form': form})


# Add email to the default user creation form
class UsrCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)


def sign_up_view(request):
    if request.method == 'POST':
        form = UsrCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            from django.core.mail import send_mail
            send_mail(
                'Thanks for joining us!',
                'You have been registered successfully.',
                'noreply@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return HttpResponseRedirect('/blog/')
    else:
        form = UsrCreationForm()

    return render(request, 'registration/sign_up.html', context={'form': form})


class BlogPostCreate(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'blog.add_blogpost'
    model = BlogPost
    fields = ['title', 'txt']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogPostUpdate(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'blog.change_blogpost'
    model = BlogPost
    fields = ['title', 'txt']
