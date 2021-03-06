from django import forms
from django.template.defaultfilters import slugify
from django.contrib.auth.forms import UserCreationForm

# import models
from django.contrib.auth.models import User
from core.models import Follow, Pin, Board

# import stream feed manager
from core.feed_managers import manager


class PinForm(forms.ModelForm):
    board_name = forms.CharField()
    remove = forms.IntegerField(required=False)

    class Meta:
        model = Pin
        exclude = ['board']

    def save(self, *args, **kwargs):
        board_name = self.cleaned_data['board_name']
        user = self.cleaned_data['user']
        remove = bool(int(self.cleaned_data.get('remove', 0) or 0))
        item = self.cleaned_data['item']

        if remove:
            pins = Pin.objects.filter(
                user=user, item=self.cleaned_data['item'])
            for pin in pins:
                manager.remove_pin(pin)
                pin.delete()
            item.pin_count -= 1
            item.save()
            print("Save removed", pin)
            return

        # create the board with the given name
        defaults = dict(slug=slugify(board_name))
        board, created = Board.objects.get_or_create(
            user=user, name=board_name, defaults=defaults)

        # save the pin
        pin = forms.ModelForm.save(self, commit=False)
        pin.board = board

        item.pin_count += 1
        item.save()
        pin.save()

        # forward the pin to manager
        manager.add_pin(pin)
        print("Save", pin)
        return pin


class FollowForm(forms.Form):
    user = forms.IntegerField()
    target = forms.IntegerField()
    remove = forms.CharField(required=False)

    def save(self):
        user = self.cleaned_data['user']
        target = self.cleaned_data['target']
        remove = True if self.cleaned_data['remove'] == u'Unfollow' else False

        if remove:
            follows = Follow.objects.filter(user=user, target=target)
            for follow in follows:
                manager.unfollow_user(follow.user_id, follow.target_id)
                follow.delete()
            return

        follow = Follow.objects.create(user_id=user, target_id=target)
        manager.follow_user(follow.user_id, follow.target_id)
        return follow


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', )


class NewpostForm(forms.Form):
    message = forms.CharField(label='Message', required=True)
    image = forms.ImageField(label='')
    # source_url = forms.CharField(label='Source URL', required=False)
