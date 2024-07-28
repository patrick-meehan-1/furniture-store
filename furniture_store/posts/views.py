from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
from .forms import CommentForm
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.db.models import Q


class PostPageView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = "all_posts_list"

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = ['title', 'body', 'category']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'body']

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,  DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    
class SearchPostsListView(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )

def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        author = request.user
        comment = form.cleaned_data['comment']
        commentObject = Comment(post=post, comment=comment, author=author)
        commentObject.save()
        
        return redirect('posts')
    
    form = CommentForm()
    context = {
        "post":post,
        "form":form
    }
    return render(request, 'comment_new.html', context)