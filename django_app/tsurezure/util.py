from . import models
from django.contrib import messages
from . import error
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout

def get_user_expansion(user, request):
    """
    引数.ユーザに紐づくユーザ拡張を返却する。引数.ユーザにユーザ拡張が存在しない場合はログアウトを行いエラーを発火する。

    :param user: ユーザ
    :param request: リクエスト
    :return: ユーザ拡張
    """

    user_expansion = None
    if user is not None and user.is_authenticated:
        try:
            return models.UserExpansion.objects.get(user=user)
        except ObjectDoesNotExist:
            logout(request)
            raise error.BusinessError('ユーザ情報に問題がありますのでログアウトしました。')
    else:
        return None

def set_user_info(request, params):
    """
    引数.リクエストからユーザを取得し、ユーザ拡張を検索、その結果をパラメータに設定する。

    :param request: リクエスト
    :param params: パラメータ
    :return: None
    """

    user_expansion = get_user_expansion(request.user, request)

    params['user_expansion'] = user_expansion