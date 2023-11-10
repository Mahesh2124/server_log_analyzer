from django.urls import path
from . import views




urlpatterns = [
    path('', views.server_login_view, name='server_login'),
    path('form_render', views.form_render, name='form_render'),
    # path('form_render', views.form_render),
    path('analyze_log/', views.analyze_log, name='analyze_log'),
    # path('display_data/', views.display_data, name='display_data'),
]