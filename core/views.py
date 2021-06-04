import json
from core import forms
from django.contrib.auth.models import User
from core.models import Follow, Item, Pin
from core.feed_managers import manager
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import (
    get_user_model,
    views as auth_views
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def home(request):
    context = RequestContext(request)
    return render_to_response('core/home.html', context)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    return auth_views.LoginView.as_view(
        template_name='registration/login.html',
        success_url="/home/")


class RegisterView(FormView):
    form_class = forms.RegisterForm
    model = UserCreationForm
    template_name = 'registration/register.html'
    success_url = "/login"

    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)


@login_required(login_url='/login/')
def trending(request):
    '''
    The most popular items
    '''
    context = RequestContext(request)

    if request.method == 'POST':
        newpost_form = forms.NewpostForm(request.POST, request.FILES)
        if newpost_form.is_valid():
            obj = Item()
            obj.user = request.user
            obj.image = newpost_form.cleaned_data['image']
            obj.message = newpost_form.cleaned_data['message']
            if 'source_url' in newpost_form.cleaned_data:
                obj.source_url = newpost_form.cleaned_data['source_url']
            else:
                obj.source_url = "www.google.com"
            obj.save()
            return HttpResponseRedirect('/')
    else:
        newpost_form = forms.NewpostForm()

    context['form'] = newpost_form

    # show a few items
    popular = Item.objects.all().order_by('-id')[:50]
    context['popular'] = popular
    response = render_to_response('core/trending.html', context)
    return response


@login_required(login_url='/login/')
def feed(request):
    '''
    Items pinned by the people you follow
    '''
    context = RequestContext(request)
    feed = manager.get_feeds(request.user.id)['normal']
    if request.REQUEST.get('delete'):
        feed.delete()
    activities = list(feed[:25])
    if request.REQUEST.get('raise'):
        raise Exception, activities
    context['feed_pins'] = enrich_activities(activities)
    response = render_to_response('core/feed.html', context)
    return response


@login_required(login_url='/login/')
def aggregated_feed(request):
    '''
    Items pinned by the people you follow
    '''
    context = RequestContext(request)
    feed = manager.get_feeds(request.user.id)['aggregated']
    if request.REQUEST.get('delete'):
        feed.delete()
    activities = list(feed[:25])
    if request.REQUEST.get('raise'):
        raise Exception, activities
    context['feed_pins'] = enrich_aggregated_activities(activities)
    response = render_to_response('core/aggregated_feed.html', context)
    return response


@login_required(login_url='/login/')
def profile(request, username):
    '''
    Shows the users profile
    '''
    context = RequestContext(request)
    context['profile_user'] = get_user_model().objects.get(username=username)

    # following and followers
    followers = Follow.objects.filter(
        target=context['profile_user'].id)
    context['followers'] = followers.count()
    context['following'] = Follow.objects.filter(
        user=context['profile_user']).count()
    
    context['is_following'] = (True 
        if request.user in [f.user for f in followers] else False)

    feed = manager.get_user_feed(context['profile_user'].id)
    if request.REQUEST.get('delete'):
        feed.delete()
    activities = list(feed[:25])
    context['profile_pins'] = enrich_activities(activities)
    response = render_to_response('core/profile.html', context)
    return response


@login_required(login_url='/login/')
def pin(request):
    '''
    Simple view to handle (re) pinning an item
    '''
    output = {}
    if request.method == "POST":
        data = request.POST.copy()
        data['user'] = request.user.id
        form = forms.PinForm(data=data)

        if form.is_valid():
            pin = form.save()
            if pin:
                output['pin'] = dict(id=pin.id)
            if not request.GET.get('ajax'):
                return redirect_to_next(request)
        else:
            output['errors'] = dict(form.errors.items())

    else:
        form = forms.PinForm()

    return render_output(output)


def redirect_to_next(request):
    return HttpResponseRedirect(request.REQUEST.get('next', '/'))


def render_output(output):
    ajax_response = HttpResponse(
        json.dumps(output), content_type='application/json')
    return ajax_response


@login_required(login_url='/login/')
def follow(request):
    '''
    A view to follow other users
    '''
    output = {}
    target = request.user
    if request.method == "POST":
        data = request.POST.copy()
        data['user'] = request.user.id
        form = forms.FollowForm(data=data)

        if form.is_valid():
            target = User.objects.get(pk=form.cleaned_data['target'])
            follow = form.save()
            if follow:
                output['follow'] = dict(id=follow.id)
        else:
            output['errors'] = dict(form.errors.items())
    else:
        form = forms.FollowForm()
    return HttpResponseRedirect('/profile/' + target.username)


def enrich_activities(activities):
    '''
    Load the models attached to these activities
    (Normally this would hit a caching layer like memcached or redis)
    '''
    pin_ids = [a.object_id for a in activities]
    pin_dict = Pin.objects.in_bulk(pin_ids)
    for a in activities:
        a.pin = pin_dict.get(a.object_id)
    return activities


def enrich_aggregated_activities(aggregated_activities):
    '''
    Load the models attached to these aggregated activities
    (Normally this would hit a caching layer like memcached or redis)
    '''
    pin_ids = []
    for aggregated_activity in aggregated_activities:
        for activity in aggregated_activity.activities:
            pin_ids.append(activity.object_id)

    pin_dict = Pin.objects.in_bulk(pin_ids)
    for aggregated_activity in aggregated_activities:
        for activity in aggregated_activity.activities:
            activity.pin = pin_dict.get(activity.object_id)
    return aggregated_activities
