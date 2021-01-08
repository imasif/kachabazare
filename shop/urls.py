from django.urls import path
from . import views

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('signup/', views.signup.as_view(), name="signup"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='products details'),
]