from django.urls import path
from . import views

app_name = 'pointage'

urlpatterns = [
    path('', views.pointage, name='pointage' ),
    path('detail/',views.detail, name='detail'),
    path('add_pointage/<int:pk>', views.add_pointage, name='add_pointage'),
    path('synthese_mensuelle/<int:pk>', views.synthese_mensuelle, name='synthese_mensuelle'),
    path('getPointage/<int:pk>',views.getPointage, name='getPointage'),

]