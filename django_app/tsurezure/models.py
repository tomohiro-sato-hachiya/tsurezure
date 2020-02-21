from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from markdownx.models import MarkdownxField

def path_icon(instance, filename):
    """
    ユーザ全般写真のパスを返却する。

    :param instance: ユーザ
    :return: パス
    """

    username = instance.user.username
    return 'images/user/{0}/{1}'.format(username, filename)

class UserExpansion(models.Model):
    """
    ユーザ拡張。Userモデルには存在しない属性を宣言するためのモデル。

    Attributes
    ----------
    user : User
        ユーザ。
    profile : str
        プロフィール。
    icon : file
        アイコン。
    """

    class Meta:
        db_table = 'user_expansion'

    user = models.OneToOneField(
        User,
        primary_key=True,
        db_index=True,
        on_delete=models.CASCADE,
    )
    profile = models.TextField(
        max_length=500,
        blank=True,
        null=True,
    )
    icon = ProcessedImageField(
        blank=True,
        null=True,
        upload_to=path_icon,
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 100},
    )

class Article(models.Model):
    """
    記事。

    Attributes
    ----------
    contributor : UserExpansion
        投稿者。
    title : str
        タイトル。
    text : str
        本文。
    created_at : DateTime
        投稿日時。
    updated_at : DateTime
        更新日時。
    """

    class Meta:
        db_table = 'article'

    contributor = models.ForeignKey(
        UserExpansion,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=30,
    )
    text = MarkdownxField(
        '本文',
        help_text='Markdown形式でご記入ください。',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

class Comment(models.Model):
    """
    コメント

    Attributes
    ----------
    article : Article
        記事。
    commenter : UserExpansion
        コメンター。
    text : str
        コメント文。
    created_at : DateTime
        投稿日時。
    """

    class Meta:
        db_table = 'comment'

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )
    commenter = models.ForeignKey(
        UserExpansion,
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        max_length=500,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )