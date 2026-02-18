from django import forms
from django.contrib.auth.models import User
from .models import Tweet

class TweetForm(forms.ModelForm):
    content = forms.CharField(
        max_length=280,
        widget=forms.Textarea(attrs={
            'placeholder': "What's happening?",
            'rows': 3,
            'class': 'composer-input',
            'id': 'tweet-content',
        }),
    )

    class Meta:
        model = Tweet
        fields = ['content']

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
