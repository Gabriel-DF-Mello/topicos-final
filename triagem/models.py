from __future__ import unicode_literals

import os

from django.conf import settings
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from utils.gerador_hash import gerar_hash

class Triagem(models.Model):
    codigo = models.CharField(_('Código da triagem *'), unique=True, max_length=20, help_text='* Campos obrigatórios')
    data = models.DateField(_('Data da triagem *'), max_length=11, help_text='dd/mm/aaaa')
    hora = models.CharField(_('Hora da triagem *'), max_length=5, help_text='hh:mm')
    nome = models.CharField(_('Nome do paciente *'), max_length=100)
    idade = models.IntegerField(_('Idade do paciente *'))
    altura = models.DecimalField(_('Altura do paciente *'), decimal_places=2, max_digits=4)
    peso = models.DecimalField(_('Peso do paciente *'), decimal_places=2, max_digits=6)
    imc = models.DecimalField(_('IMC do paciente *'), decimal_places=2, max_digits=4)
    q1 = models.BooleanField(_('Tem febre? *'))
    q2 = models.BooleanField(_('Tem dor de cabeça? *'))
    q3 = models.BooleanField(_('Tem secreção nasal ou espirros? *'))
    q4 = models.BooleanField(_('Tem dor/irritação na garganta? *'))
    q5 = models.BooleanField(_('Tem tosse seca? *'))
    q6 = models.BooleanField(_('Tem dificuldade respiratória? *'))
    q7 = models.BooleanField(_('Tem dores no corpo? *'))
    q8 = models.BooleanField(_('Tem diarréia? *'))
    q9 = models.BooleanField(_('Viajou nos últimos 14 dias para local com casos confirmados de COVID-19? *'))
    q10 = models.BooleanField(_('Esteve em contato, nos últimos 14 dias com um caso diagnosticado de COVID-19? *'))
    risco = models.IntegerField(_('Risco do paciente *'))

    atendente = models.ForeignKey('usuario.Usuario', null=True, blank=True, verbose_name='Atendente *',
                                on_delete=models.PROTECT, related_name='atendente')

    slug = models.SlugField('Hash', max_length=200, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering            =   ['-data','-hora']
        verbose_name        =   ('triagem')
        verbose_name_plural =   ('triagens')
        unique_together     =   ['codigo', 'data', 'hora'] #criando chave primária composta no BD

    def __str__(self):
        return "Ata: %s. Data: %s." % (self.codigo, self.data)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        self.codigo = self.codigo.upper()
        super(Triagem, self).save(*args, **kwargs)

    @property
    def get_delete_url(self):
        return reverse('triagem_delete', args=[str(self.id)])

    @property
    def get_visualiza_url(self):
        return reverse('triagem_detail', args=[str(self.id)])