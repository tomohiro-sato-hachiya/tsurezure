from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('top/', views.TopView.as_view(), name='top'),
    path('top/<int:page>/', views.TopView.as_view(), name='top'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('article-create/', views.ArticleCreateView.as_view(), name='article-create'),
    path('article-detail/<int:article_id>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('user/<username>/', views.UserView.as_view(), name='user'),
    path('user/<username>/<int:page>/', views.UserView.as_view(), name='user'),
    path('my-articles/', views.MyArticlesView.as_view(), name='my-articles'),
    path('my-articles/<int:page>/', views.MyArticlesView.as_view(), name='my-articles'),
    path('article-update/<int:article_id>/', views.ArticleUpdateView.as_view(), name='article-update'),
    path('password-confirmation/', views.PasswordConfirmationView.as_view(), name='password-confirmation'),
    path('user-update/', views.UserUpdateView.as_view(), name='user-update'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password-change'),
]
