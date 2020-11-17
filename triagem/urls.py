from django.conf.urls import url

from .views import TriagemListView, TriagemCreateView, TriagemDetailView
from .views import TriagemDeleteView


urlpatterns = [
	url(r'list/$', TriagemListView.as_view(), name='triagem_list'),
	url(r'cad/$', TriagemCreateView.as_view(), name='triagem_create'),
	url(r'(?P<pk>\d+)/detalhes/$', TriagemDetailView.as_view(), name='triagem_detail'),
	url(r'(?P<pk>\d+)/delete/$', TriagemDeleteView.as_view(), name='triagem_delete'),
]
