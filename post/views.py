from post.models import Post,Like,Save,Comment,Reply
from message.models import Message, Inbox
from post.forms import PostForm, CommentForm
from post.owner import  OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

from notification.models import LikeNotification, CommentNotification, InboxNotification

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



@login_required
def PostListView(request):
    template_name = "post/post_list.html"

    context = {}

    following_queryset = request.user.following.all()
    following = [follow.reciever for follow in following_queryset]
    posts = Post.objects.filter(owner__in = following).order_by('-created_at')
    
    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj

    comment_form = CommentForm()
    context['comment_form'] = comment_form

    rows = request.user.like_post.values('id')
    liked_posts = [ row['id'] for row in rows ]
    context['liked_posts'] = liked_posts

    rows = request.user.save_post.values('id')
    saved_posts = [ row['id'] for row in rows ]
    context['saved_posts'] = saved_posts

    return render(request, template_name, context)



class PostCreateView(OwnerCreateView):
    model = Post
    template_name = "post/post_create.html"
    form_class = PostForm

    def get_success_url(self):
        return reverse('post_list')



@login_required
def CommentCreateView(request, pk):
    post = Post.objects.get(id=pk)
    response_data = {}
    
    if request.POST.get('action') == 'post':
        text = request.POST.get('text')
        comment = Comment.objects.create(
            text = text,
            owner = request.user,
            post = post,
        )

        if comment.owner != post.owner:
            notification = CommentNotification.objects.get_or_create(comment=comment)

        response_data['text'] = text
        response_data['created_at'] = comment.created_at
        response_data['owner'] = comment.owner.username
        response_data['photo'] = comment.owner.user.photo.url
        response_data['comment_id'] = comment.id
        response_data['post_id'] = pk

        return JsonResponse(response_data)    

    return redirect('post_list') 

@login_required
def ReplyCreateView(request, pk):
    comment = Comment.objects.get(id=pk)
    response_data = {}
    
    if request.POST.get('action') == 'post':
        text = request.POST.get('text')
        reply = Reply.objects.create(
            text = text,
            owner = request.user,
            comment = comment,
        )

        response_data['text'] = text
        response_data['created_at'] = reply.created_at
        response_data['owner'] = reply.owner.username
        response_data['photo'] = reply.owner.user.photo.url
        response_data['comment_id'] = pk
        response_data['post_id'] = comment.post.id

        return JsonResponse(response_data)    

    return redirect('post_list') 


@method_decorator(csrf_exempt, name='dispatch')
@login_required
def SearchView(request):
    if request.is_ajax():
        url_parameter = request.GET.get("q")
        if url_parameter:
            profiles = User.objects.filter(username__icontains=url_parameter)
        else:
            profiles = None

        html = render_to_string(
            template_name="post/search.html", 
            context={"profiles": profiles}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict)



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
        html = render_to_string('post/single_post.html', {'user':request.user, 'post': post, 'comment_form':comment_form, 'liked_posts':liked_posts, 'saved_posts':saved_posts})
        return JsonResponse(data={'html':html})



@method_decorator(csrf_exempt, name='dispatch')
class LikeView(LoginRequiredMixin, View):

    def post(self, request, pk):
        print("Add like PK:",pk)
        post = get_object_or_404(Post, id=pk)
        like = Like(owner=request.user, post=post)
        
        try:
            like.save()  
            if like.owner != post.owner:
                notification = LikeNotification.objects.create(like=like)
        except IntegrityError:
            pass
    

        html = render_to_string('post/like_count.html', {'post': post})
        return JsonResponse(data={'html':html})



@method_decorator(csrf_exempt, name='dispatch')
class UnlikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print("Delete like PK:",pk)
        post = get_object_or_404(Post, id=pk)

        try:
            like = Like.objects.get(owner=request.user, post=post).delete()
            notification = LikeNotification.objects.get(like=like).delete()
        except (Like.DoesNotExist, LikeNotification.DoesNotExist) as e:
            pass

        html = render_to_string('post/like_count.html', {'post': post})
        return JsonResponse(data={'html':html})



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
        except Save.DoesNotExist:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
@login_required
def ShareProfileView(request):
    if request.is_ajax():
        url_parameter = request.GET.get("q")
        if url_parameter:
            profiles = User.objects.filter(first_name__icontains=url_parameter)
        else:
            profiles = None

        html = render_to_string(
            template_name="post/share_profile_search.html", 
            context={"profiles": profiles}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict)



@method_decorator(csrf_exempt, name='dispatch')
class ShareView(LoginRequiredMixin, View):

    def post(self, request):
        
        profile_id = request.POST.get('profile_id')
        post_id = request.POST.get('post_id')

        owner_inbox = Inbox.objects.get_or_create(owner=self.request.user, reciever=User.objects.get(id=profile_id))[0]
        reciever_inbox = Inbox.objects.get_or_create(owner=User.objects.get(id=profile_id), reciever=self.request.user)[0]
        post = get_object_or_404(Post, id=post_id)

        message = Message.objects.create(post=post,owner_inbox=owner_inbox, reciever_inbox=reciever_inbox)

        notification = InboxNotification.objects.get_or_create(inbox=reciever_inbox)[0]

        return HttpResponse()



class ExploreView(OwnerListView):
    context_object_name = "posts"
    template_name = "post/explore.html"
    model = Post
    ordering = ['-created_at']
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(OwnerListView, self).get_context_data(**kwargs)

        rows = self.request.user.like_post.values('id')
        liked_posts = [ row['id'] for row in rows ]
        context['liked_posts'] = liked_posts

        rows = self.request.user.save_post.values('id')
        saved_posts = [ row['id'] for row in rows ]
        context['saved_posts'] = saved_posts

        return context
    

