from rest_framework.exceptions import AuthenticationFailed

from notifications.models import Company, Target


def get_company_from_headers(request):
    """
    Extrai e valida o header X-Api-Key.
    Retorne a Empresa correspondente.
    """
    api_key = request.headers.get('X-Api-Key')

    if not api_key:
        raise AuthenticationFailed('Header X-Api-Key e obrigatório.')

    try:
        company = Company.objects.get(hash=api_key)
    except Company.DoesNotExist:
        raise AuthenticationFailed('X-Api-Key inválida.')

    return company

def get_target_from_headers(request):
    """
    Extrai e valida o headers X-Api-Key e X-User-Id.
    Retorna o Target correspondente.
    """

    company = get_company_from_headers(request)

    user_id = request.headers.get('X-User-Id')

    if not user_id:
        raise AuthenticationFailed('Header X-User-Id e obrigatorio.')

    # Busca ou cria o target (usuário nessa empresa)
    target, created = Target.objects.get_or_create(company=company, user_id=user_id)
    return target

