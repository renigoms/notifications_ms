import secrets

from django.db import models

# Create your models here.
class Company(models.Model):
    """
    Representa um sistema/cliente que usa o microservico.
    Cada empresa recebe um hash único de 16 caracteres para autenticação.
    """

    name = models.CharField(max_length=200, unique=True)
    hash = models.CharField(max_length=16, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = secrets.token_hex(8)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name

class Target(models.Model):
    """
    Vincula um usuário de um sistema externo ao microserviço.
    O user_id e o ID do usuário no sistema cliente (ex: User.id do portfolio).
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='targets')
    user_id = models.IntegerField()

    class Meta:
        verbose_name = 'Target'
        verbose_name_plural = 'Targets'
        unique_together = ['company', 'user_id']

    def __str__(self):
        return f'{self.company.name} - User {self.user_id}'

class Notification(models.Model):
    """
    Uma notificação enviada para um target específico.
    """
    title = models.CharField(max_length=200, default='Título')
    target = models.ForeignKey(Target, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification',
        verbose_name_plural = 'Notifications',
        ordering = ['-create_at',]

    def __str__(self):
        status = 'Lida' if self.is_read else 'Não Lida'
        return f'[{status}] {self.message[:50]}'