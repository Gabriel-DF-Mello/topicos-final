from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from datetime import timedelta, datetime

from utils.gerador_hash import gerar_hash

# Create your models here.
class AdministradorAtivoManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo='ADMINISTRADOR', is_active=True)


class EnfermeiroAtivoManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(tipo='ENFERMEIRO', is_active=True)


class Usuario(AbstractBaseUser):

    # 1 campo da tupla fica no banco de dados
    # 2 campo da tupla eh mostrado para o usuario

    TIPOS_USUARIOS = (
        ('ADMINISTRADOR', 'Administrador'),
        ('ENFERMEIRO', 'Enfermeiro'),
    )

    USERNAME_FIELD = 'email'

    tipo = models.CharField(_('Tipo do usuário *'), max_length=15, choices=TIPOS_USUARIOS, default='PROFESSOR', help_text='* Campos obrigatórios')
    nome = models.CharField(_('Nome completo *'), max_length=100)
    email = models.EmailField(_('Email'), unique=True, max_length=100, db_index=True)
    celular = models.CharField(_('Telefone celular'), max_length=30)
    endereco = models.CharField(_('Endereço'), max_length=100)

    is_active = models.BooleanField(_('Ativo'), default=False, help_text='Se ativo, o usuário tem permissão para acessar o sistema')
    slug = models.SlugField('Hash', max_length=200, null=True, blank=True)

    objects = UserManager()
    administradores = AdministradorAtivoManager()
    enfermeiros = EnfermeiroAtivoManager()

    class Meta:
        ordering            =   ['nome']
        verbose_name        =   ('usuário')
        verbose_name_plural =   ('usuários')

    def __str__(self):
        return self.nome

    def get_email(self):
        return self.email

    def get_celular(self):
        return self.celular

    def get_id(self):
        return self.id

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        self.nome = self.nome.upper()
        if not self.id:
            self.set_password(self.password) #criptografa a senha digitada no forms
        super(Usuario, self).save(*args, **kwargs)

    @property
    def is_adm(self):
        if self.tipo == 'ADMINISTRADOR':
            return True
        return False

    @property
    def get_absolute_url(self):
        return reverse('usuario_update', args=[str(self.id)])

    @property
    def get_delete_url(self):
        return reverse('usuario_delete', args=[str(self.id)])

    @property
    def get_usuario_register_activate_url(self):
        return '%s%s' % (settings.DOMINIO_URL, reverse('usuario_register_activate', kwargs={'slug': self.slug}))
