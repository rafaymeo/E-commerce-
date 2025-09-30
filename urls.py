from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.index_view, name='index'),
     path('logout/', views.logout_view, name='logout'),  # ← Add this
     path('product/', views.product_detail_view, name='product_detail'),
    path("contact/", views.contact_view, name="contact"),
]

