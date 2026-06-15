from django.urls import path

from notifications import views

urlpatterns = [
    path(
        'api/notificacoes/nao-lidas/',
        views.UnreadNotificationsCountView.as_view(),
        name='unread-notifications'
    ),
    path(
        'api/notificacoes/',
        views.NotificationsListView.as_view(),
        name='notifications-list'
    ),

    path(
        'api/notificacoes/criar/',
        views.NotificationCreateView.as_view(),
        name='notification-create'
    ),

    path(
        'api/notificacoes/<int:pk>/lida/',
        views.NotificationMarkAsReadView.as_view(),
        name='notification-mark-as-read'
    ),

]