from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.forms.models import inlineformset_factory
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View

from .models import Profile
from .forms import UserEditForm, ProfileEditForm, SignUpForm

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

def signupView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request,'user/signup.html', {'form':form})


@method_decorator(csrf_exempt, name='dispatch')
class followView(View):

    def post(self, request):
        user_name = request.POST.get('username')
        user2 = User.objects.get(username=user_name)

        if(user2 in request.user.user.following.all()):
            u = request.user.user.following.remove(user2)
        else:
            u = request.user.user.following.add(user2)

        following_queryset = request.user.user.following.all()
        following = [user.username for user in following_queryset]
                
        html = render_to_string(
            template_name="user/follow.html", 
            context={'following':following, 'profile':user2}
        )
        response_data = {}
        response_data['html'] = html
        return JsonResponse(response_data)    


def profileView(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    following_queryset = request.user.user.following.all()
    following = [user.username for user in following_queryset]
    return render(request, 'user/profile.html',{'profile':profile,'following':following})



@login_required
def editView(request):

    if request.method == 'POST':
        u_form = UserEditForm(request.POST, instance=request.user)
        p_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.user)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('edit')
    else:
        u_form = UserEditForm(instance=request.user)
        p_form = ProfileEditForm(instance=request.user.user)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request, 'user/edit.html', context)



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please make sure both passwords match')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {
        'form': form
    })