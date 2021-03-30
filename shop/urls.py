import debug_toolbar
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('categories/', views.cat.as_view(), name='category'),
    path('categories/<slug:pk>', views.catDetails.as_view(), name='category'),
    path('signup/', views.signup.as_view(), name="signup"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name='products_details'),
    path('__debug__/', include(debug_toolbar.urls)),
]