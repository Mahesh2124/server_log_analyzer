from django.urls import path
from . import views
from .views import EraseDataView




urlpatterns = [
    path('', views.server_login_view, name='server_login'),
    path('server_details/',views.server_details,name='server_details'),
    path('form_render/', views.form_render, name='form_render'),
    path('analyze_log/', views.analyze_log, name='analyze_log'),
   path('erase_data/', EraseDataView.as_view(), name='erase_data'),
   path('date_logs/',views.date_logs,name='date_logs'),
]