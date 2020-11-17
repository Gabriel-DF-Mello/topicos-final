from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin,  StaffRequiredMixin

from .models import Triagem


class TriagemListView(LoginRequiredMixin, ListView):
    model = Triagem


class TriagemCreateView(LoginRequiredMixin, CreateView):
    model = Triagem
    fields = ['codigo', 'atendente', 'data', 'hora', 'nome', 'idade', 'altura', 'peso', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']
    success_url = 'triagem_list'

    def form_valid(self, form):
        triagem = form.instance
        pontos = 0

        if triagem.q1:
            pontos += 5

        if triagem.q2:
            pontos += 1

        if triagem.q3:
            pontos += 1

        if triagem.q4:
            pontos += 1

        if triagem.q5:
            pontos += 3

        if triagem.q6:
            pontos += 10

        if triagem.q7:
            pontos += 1

        if triagem.q8:
            pontos += 1

        if triagem.q9:
            pontos += 3

        if triagem.q10:
            pontos += 10

        if pontos == 0:
            triagem.risco = 0

        elif pontos >= 1  and pontos < 10:
            triagem.risco = 1

        elif pontos >= 10 and pontos < 20:
            triagem.risco = 2

        elif pontos >= 20:
            triagem.risco = 3

        form.save()
        return super(TriagemCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Ata cadastrada com sucesso na plataforma!')
        return reverse(self.success_url)


class TriagemDeleteView(LoginRequiredMixin, DeleteView):
    model = Triagem
    success_url = 'triagem_list'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à essa ata, permissão negada!')
        return redirect(self.success_url)


class TriagemDetailView(LoginRequiredMixin, DetailView):
    model = Triagem
    template_name = 'triagem/triagem_detail.html'