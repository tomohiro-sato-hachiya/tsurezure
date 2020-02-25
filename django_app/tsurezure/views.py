from django.shortcuts import render, redirect
from . import forms
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from . import util
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from . import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import Http404

class RegisterView(TemplateView):
    def __init__(self):
        self.params = {
            'title': 'ユーザ登録',
            'register_form' : forms.RegisterForm(),
            'user_expansion_form' : forms.UserExpansionForm(),
        }

    def get(self, request):
        util.set_user_info(request, self.params)
        return render(request, 'tsurezure/register.html', self.params)

    def post(self, request):
        util.set_user_info(request, self.params)
        register_form = forms.RegisterForm(request.POST)
        user_expansion_form = forms.UserExpansionForm(request.POST, request.FILES)

        if register_form.is_valid() and user_expansion_form.is_valid():
            user = register_form.save()
            user_expansion = user_expansion_form.save(commit=False)
            user_expansion.user = user
            user_expansion.save()
            login(request, user)
            messages.success(request, 'ユーザ登録に成功しました。')
            return redirect(to='/tsurezure/top')
        else:
            self.params['register_form'] = register_form
            self.params['user_expansion_form'] = user_expansion_form
            messages.error(request, 'ユーザ登録に失敗しました。')
            return render(request, 'tsurezure/register.html', self.params)


class TopView(TemplateView):
    def __init__(self):
        self.params = {
            'title': 'トップ',
            'paginator_url': 'top'
        }

    def get(self, request, page=1):
        util.set_user_info(request, self.params)
        data = models.Article.objects.all().order_by('created_at').reverse()
        self.params['articles'] = Paginator(data, 10).get_page(page)
        return render(request, 'tsurezure/top.html', self.params)


class LoginView(TemplateView):
    def __init__(self):
        self.params = {
            'title': 'ログイン',
            'form' : forms.LoginForm(),
        }

    def get(self, request):
        util.set_user_info(request, self.params)
        return render(request, 'tsurezure/login.html', self.params)

    def post(self, request):
        util.set_user_info(request, self.params)
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            next_url = '/tsurezure/top'
            if 'next' in request.POST and request.POST['next'] != '':
                next_url = request.POST['next']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                request,
                username=username,
                password=password
            )
            login(request, user)
            messages.success(request, 'ログインに成功しました。')

            return redirect(to=next_url)
        else:
            messages.error(request, 'ログインに失敗しました。')
            self.params['form'] = form
            return render(request, 'tsurezure/login.html', self.params)


class ArticleCreateView(TemplateView):
    def __init__(self):
        self.params = {
            'title': '記事投稿',
            'form': forms.ArticleForm(),
            'article_form_url': 'article-create',
        }

    @method_decorator(login_required)
    def get(self, request):
        util.set_user_info(request, self.params)
        return render(request, 'tsurezure/article-create.html', self.params)

    @method_decorator(login_required)
    def post(self, request):
        util.set_user_info(request, self.params)
        form = forms.ArticleForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.contributor = util.get_user_expansion(request.user, request)
            article.save()
            messages.success(request, '記事投稿に成功しました。')
            redirect_url = '/tsurezure/article-detail/' + str(article.id) + '/'
            return redirect(to=redirect_url)
        else:
            self.params['form'] = form
            messages.error(request, '記事投稿に失敗しました。')
            return render(request, 'tsurezure/article-create.html', self.params)


class ArticleDetailView(TemplateView):
    def __init__(self):
        self.params = {
            'title': '記事閲覧',
            'form': forms.CommentForm(),
        }

    def get(self, request, article_id):
        util.set_user_info(request, self.params)
        try:
            article = models.Article.objects.get(id=article_id)
            self.params['article'] = article
            self.params['comments'] = models.Comment.objects.filter(article=article).order_by('created_at').reverse()
            self.params['next_url'] = '/tsurezure/article-detail/' + str(article_id) + '/'
            return render(request, 'tsurezure/article-detail.html', self.params)
        except ObjectDoesNotExist:
            messages.error(request, '指定した記事が存在しません。')
            raise Http404

    @method_decorator(login_required)
    def post(self, request, article_id):
        util.set_user_info(request, self.params)

        try:
            article = models.Article.objects.get(id=article_id)
            form = forms.CommentForm(request.POST)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.commenter = util.get_user_expansion(request.user, request)
                comment.article = article
                comment.save()
                messages.success(request, 'コメント投稿に成功しました。')
                redirect_url = '/tsurezure/article-detail/' + str(article_id) + '/'
                return redirect(to=redirect_url)
            else:
                self.params['form'] = form
                self.params['comments'] = models.Comment.objects.filter(article=article).order_by(
                    'created_at').reverse()
                self.params['next_url'] = '/tsurezure/article-detail/' + str(article_id) + '/'
                messages.error(request, 'コメント投稿に失敗しました。')
                return render(request, 'tsurezure/article-detail.html', self.params)
        except ObjectDoesNotExist:
            messages.error(request, '指定した記事が存在しません。')
            raise Http404

class UserView(TemplateView):
    def __init__(self):
        self.params = {
            'title': 'ユーザ',
        }

    def get(self, request, username, page=1):
        util.set_user_info(request, self.params)

        try:
            watch_user = User.objects.get(username=username)
            watch_user_expansion = util.get_user_expansion(watch_user, request)
            self.params['watch_user_expansion'] = watch_user_expansion

            data = models.Article.objects.filter(contributor=watch_user_expansion).order_by('created_at').reverse()
            self.params['articles'] = Paginator(data, 10).get_page(page)

            return render(request, 'tsurezure/user.html', self.params)
        except ObjectDoesNotExist:
            messages.error(request, '指定したユーザが存在しません。')
            raise Http404

class MyArticlesView(TemplateView):
    def __init__(self):
        self.params = {
            'title': '投稿記事',
            'paginator_url': 'my-articles',
        }

    @method_decorator(login_required)
    def get(self, request, page=1):
        util.set_user_info(request, self.params)

        user_expansion = util.get_user_expansion(request.user, request)
        data = models.Article.objects.filter(contributor=user_expansion).order_by('created_at').reverse()
        self.params['articles'] = Paginator(data, 10).get_page(page)

        return render(request, 'tsurezure/my-articles.html', self.params)

class ArticleUpdateView(TemplateView):
    def __init__(self):
        self.params = {
            'title': '投稿記事の編集',
        }

    @method_decorator(login_required)
    def get(self, request, article_id):
        util.set_user_info(request, self.params)

        user_expansion = util.get_user_expansion(request.user, request)
        try:
            article = models.Article.objects.get(id=article_id, contributor=user_expansion)
            self.params['article'] = article
            self.params['form'] = forms.ArticleForm(instance=article)
            self.params['article_id'] = article_id

            return render(request, 'tsurezure/article-update.html', self.params)
        except ObjectDoesNotExist:
            messages.error(request, '指定した記事が存在しないか、自分の投稿記事ではありません。')
            raise Http404

    @method_decorator(login_required)
    def post(self, request, article_id):
        util.set_user_info(request, self.params)

        user_expansion = util.get_user_expansion(request.user, request)
        try:
            article = models.Article.objects.get(id=article_id, contributor=user_expansion)
            form = forms.ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                messages.success(request, '記事更新に成功しました。')
                redirect_url = '/tsurezure/article-detail/' + str(article_id) + '/'
                return redirect(to=redirect_url)
            else:
                self.params['article'] = article
                self.params['form'] = form
                self.params['article_id'] = article_id
                messages.error(request, '記事更新に失敗しました。')
                return render(request, 'tsurezure/article-update.html', self.params)
        except ObjectDoesNotExist:
            messages.error(request, '指定した記事が存在しないか、自分の投稿記事ではありません。')
            raise Http404


class PasswordConfirmationView(TemplateView):
    def __init__(self):
        self.params = {
            'title': 'パスワードの確認',
            'form': forms.PasswordConfirmationForm(),
            'wrong_password_flg': False,
        }

    def get(self, request):
        util.set_user_info(request, self.params)

        user_expansion = util.get_user_expansion(request.user, request)
        if user_expansion is not None:
            return render(request, 'tsurezure/password-confirmation.html', self.params)
        else:
            return redirect(to='/tsurezure/login?next=user-update')

    @method_decorator(login_required)
    def post(self, request):
        util.set_user_info(request, self.params)

        form = forms.PasswordConfirmationForm(request.POST)
        self.params['form'] = form

        if form.is_valid():
            if request.user.check_password(request.POST['password']):
                request.session['password_confirmed'] = True
                messages.success(request, 'パスワード確認に成功しました。')
                return redirect(to='/tsurezure/user-update')
            else:
                self.params['wrong_password_flg'] = True
                messages.error(request, 'パスワード確認に失敗しました。')
                return render(request, 'tsurezure/password-confirmation.html', self.params)
        else:
            return render(request, 'tsurezure/password-confirmation.html', self.params)


class UserUpdateView(TemplateView):
    def __init__(self):
        self.params = {
            'title': 'ユーザ情報の確認・更新',
        }

    @method_decorator(login_required)
    def get(self, request):
        util.set_user_info(request, self.params)

        if request.session.get('password_confirmed', False):
            user_expansion = util.get_user_expansion(request.user, request)
            self.params['form'] = forms.UserExpansionForm(instance=user_expansion)
            request.session['password_confirmed'] = False

            return render(request, 'tsurezure/user-update.html', self.params)
        else:
            return redirect(to='/tsurezure/password-confirmation')

    @method_decorator(login_required)
    def post(self, request):
        util.set_user_info(request, self.params)

        user_expansion = util.get_user_expansion(request.user, request)
        form = forms.UserExpansionForm(request.POST, request.FILES, instance=user_expansion)
        if form.is_valid():
            form.save()
            messages.success(request, 'ユーザ情報更新に成功しました。')
            return redirect(to='/tsurezure/user-update')
        else:
            self.params['form'] = form
            messages.error(request, 'ユーザ情報更新に失敗しました。')
            return render(request, 'tsurezure/user-update.html', self.params)

class PasswordChangeView(TemplateView):
    def __init__(self):
        self.params = {
            'title': 'パスワード変更',
        }

    @method_decorator(login_required)
    def get(self, request):
        util.set_user_info(request, self.params)

        self.params['form'] = forms.OriginalPasswordChangeForm(user=request.user)

        return render(request, 'tsurezure/password-change.html', self.params)

    @method_decorator(login_required)
    def post(self, request):
        util.set_user_info(request, self.params)

        form = forms.OriginalPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'パスワード変更に成功しました。')
            return redirect(to='/tsurezure/user-update')
        else:
            self.params['form'] = form
            messages.error(request, 'パスワード変更に失敗しました。')
            return render(request, 'tsurezure/password-change.html', self.params)
