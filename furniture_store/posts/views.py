from django.views.generic import ListView, DetailView
from .models import Post


class PostPageView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = "all_posts_list"

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'