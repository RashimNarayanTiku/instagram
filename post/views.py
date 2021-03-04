from post.models import Post,Comment,Like,Save
from post.forms import CommentForm
from post.owner import  OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

from django.core import serializers
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


class PostListView(OwnerListView):
    context_object_name = "posts"
    template_name = "post/post_list.html"
    model = Post
    ordering = ['-created_at']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(OwnerListView, self).get_context_data(**kwargs)

        comment_form = CommentForm()
        context['comment_form'] = comment_form

        rows = self.request.user.like_post.values('id')
        liked_posts = [ row['id'] for row in rows ]
        context['liked_posts'] = liked_posts

        rows = self.request.user.save_post.values('id')
        saved_posts = [ row['id'] for row in rows ]
        context['saved_posts'] = saved_posts

        return context

@login_required
def CommentCreateView(request, pk):
    post = Post.objects.get(id=pk)
    response_data = {}
    
    if request.POST.get('action') == 'post':
        text = request.POST.get('text')
        Comment.objects.create(
            text = text,
            owner = request.user,
            post = post,
        )
        response_data['text'] = text
        response_data['post_id'] = pk
        
        return JsonResponse(response_data)    
    return redirect('post_list') 


@method_decorator(csrf_exempt, name='dispatch')
@login_required
def SearchView(request):
    if request.is_ajax():
        url_parameter = request.GET.get("q")
        if url_parameter:
            profiles = User.objects.filter(first_name__icontains=url_parameter)
        else:
            profiles = None

        html = render_to_string(
            template_name="post/search.html", 
            context={"profiles": profiles}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
@login_required
def SinglePostView(request, pk):
    if request.is_ajax():
        post = get_object_or_404(Post, id=pk)
        like_rows = request.user.like_post.values('id')
        liked_posts = [ row['id'] for row in like_rows ]
        save_rows = request.user.save_post.values('id')
        saved_posts = [ row['id'] for row in save_rows ]
        comment_form = CommentForm()
        html = render_to_string('post/single_post.html', {'post': post, 'comment_form':comment_form, 'liked_posts':liked_posts, 'saved_posts':saved_posts})
        return JsonResponse(data={'html':html}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class LikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print("Add like PK:",pk)
        post = get_object_or_404(Post, id=pk)
        like = Like(owner=request.user, post=post)
        try:
            like.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        html = render_to_string('post/like_count.html', {'post': post})
        return JsonResponse(data={'html':html}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UnlikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print("Delete like PK:",pk)
        post = get_object_or_404(Post, id=pk)
        try:
            like = Like.objects.get(owner=request.user, post=post).delete()
        except Like.DoesNotExist as e:
            pass
        html = render_to_string('post/like_count.html', {'post': post})
        return JsonResponse(data={'html':html}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class SaveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print("Add save PK:",pk)
        post = get_object_or_404(Post, id=pk)
        save = Save(owner=request.user, post=post)
        try:
            save.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class UnsaveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print("Delete save PK:",pk)
        post = get_object_or_404(Post, id=pk)
        try:
            save = Save.objects.get(owner=request.user, post=post).delete()
        except Save.DoesNotExist as e:
            pass
        return HttpResponse()