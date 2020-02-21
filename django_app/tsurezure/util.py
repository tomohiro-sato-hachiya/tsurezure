from . import models
from django.contrib import messages
from . import error
from django.core.exceptions import ObjectDoesNotExist

def get_user_expansion(user):
    """
    引数.ユーザに紐づくユーザ拡張を返却する。

    :param user: ユーザ
    :return: ユーザ拡張
    """

    user_expansion = None
    if user is not None and user.is_authenticated:
        try:
            return models.UserExpansion.objects.get(user=user)
        except ObjectDoesNotExist:
            raise error.BusinessError('ユーザ情報に問題があります')
    else:
        return None

def set_user_info(request, params):
    """
    引数.リクエストからユーザを取得し、ユーザ拡張を検索、その結果をパラメータに設定する。

    :param request: リクエスト
    :param params: パラメータ
    :return: None
    """

    user_expansion = get_user_expansion(request.user)

    params['user_expansion'] = user_expansion