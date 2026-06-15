from django.db.models import Model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.authentication import get_target_from_headers, get_company_from_headers
from notifications.models import Notification, Target
from notifications.serializers import NotificationSerializer, NotificationCreateSerializer


# Create your views here.

class UnreadNotificationsCountView(APIView):
    """
    GET /api/notificacoes/nao-lidas/
    Retorna a quantidade de notificações não lidas do usuário
    """

    def get(self, request):
        target = get_target_from_headers(request)
        count = Notification.objects.filter(target=target).count()
        return Response({'count': count})

class NotificationsListView(APIView):
    """
    GET /api/notificacoes/
    Retorna as notificações do usuário.

    Query params opcionais:
        ?is_read=true; - somente lidas
        ?is_read=false; - somente não lidas
        (sem parametro) - todas
    """

    def get(self, request):
        target = get_target_from_headers(request)
        notifications = Notification.objects.filter(target=target)

        # filtro opcional por is_read
        is_read_param = request.query_params.get('is_read')
        if is_read_param is not None:
            is_read = is_read_param.lower() in ['true', '1', 'yes']
            notifications = notifications.filter(is_read=is_read)

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class NotificationMarkAsReadView(APIView):
    """
    PATCH /api/notificacoes/<id>/lida/
    Marca uma mensagem como lida.
    """

    def patch(self, request, pk):
        target = get_target_from_headers(request)

        try:
            notification = Notification.objects.get(pk=pk, target=target)
        except Notification.DoesNotExist:
            return Response({'erro': 'Notificação não encontrada'}, status=404)

        notification.is_read = True
        notification.save()

        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

class NotificationCreateView(APIView):
    """
    POST /api/notificacoes/criar/
    Criar uma notificação para o usuário.

    Esse endpoint é usado por OUTROS SISTEMAS (ou pelo admin/testes)
    para enviar notificações. O portifolio NÃO usa esse endpoint - ele
    apenas LÊ as notificações.

    Headers: X-Api-Key (identifica a empresa)
    Body: {"user_id": 1, "message": "Texto da notificação"}
    """

    def post(self, request):
        company = get_company_from_headers(request)

        serializer = NotificationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Buscar ou criar target
        target, created = Target.objects.get_or_create(company=company, user_id=serializer.validated_data['user_id'])

        # Cria a notificação
        notification = Notification.objects.create(target=target, message=serializer.validated_data['message'])

        return Response(NotificationSerializer(notification).data, status=status.HTTP_201_CREATED)