from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from . import models
from markdownx.widgets import MarkdownxWidget
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    """
    ユーザ登録を行うためのフォーム。
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = 'ユーザ名'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].label = 'パスワード'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].label = 'パスワード2(確認用)'


class UserExpansionForm(forms.ModelForm):
    """
    ユーザ拡張のフォーム。
    """

    class Meta:
        model = models.UserExpansion
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['profile'].label = 'プロフィール(500字まで)'
        self.fields['profile'].widget.attrs['class'] = 'form-control'
        self.fields['icon'].label = 'アイコン'
        self.fields['icon'].widget.attrs['class'] = 'form-control-file'


class LoginForm(AuthenticationForm):
    """
    ログインを行うためのフォーム。
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザ名'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'パスワード'


class ArticleForm(forms.ModelForm):
    """
    記事のフォーム。
    """

    class Meta:
        model = models.Article
        exclude = ['contributor']
        widgets = {
            'text': MarkdownxWidget(attrs={'class': 'textarea'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['title'].label = 'タイトル'
        self.fields['text'].widget.attrs['class'] = 'form-control'
        self.fields['text'].label = '本文'


class CommentForm(forms.ModelForm):
    """
    コメント投稿を行うためのフォーム。
    """

    class Meta:
        model = models.Comment
        exclude = ['article', 'commenter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['text'].widget.attrs['class'] = 'form-control'
        self.fields['text'].label = 'コメント文はこちらから'


class PasswordConfirmationForm(forms.Form):
    """
    パスワードを確認するためのフォーム。
    """

    password = forms.CharField(label='パスワード', widget=forms.PasswordInput(), min_length=8)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'パスワード'


class OriginalPasswordChangeForm(PasswordChangeForm):
    """
    パスワードを変更するためのフォーム。
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].widget.attrs['placeholder'] = '元のパスワード'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = '新しいパスワード'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = '新しいパスワード(確認用)'