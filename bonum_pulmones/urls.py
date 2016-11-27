from django.conf.urls import url

from bonum_pulmones import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^register/', views.register, name='register'),
    url(r'^submit/', views.submit, name='submit'),
    url(r'^get_result/(?P<measurement_id>[^/]+)/', views.get_result, name='get_result'),
    url(r'^history/', views.history, name='history'),
    url(r'', views.main, name='main'),
]
