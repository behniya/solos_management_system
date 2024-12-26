from django.urls import path
from .views import SiloListView , SiloLogView

urlpatterns = [
    path('silos/', SiloListView.as_view(), name='silo-list'),
    path('<int:silo_id>/logs/', SiloLogView.as_view(), name='silo-log'),
]