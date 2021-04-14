import debug_toolbar
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('categories/', views.cat.as_view(), name='category'),
    path('categories/<slug:pk>', views.catDetails.as_view(), name='category'),
    path('signup/', views.signup.as_view(), name="signup"),
    path('activate/<uidb>/<token>/', views.ActivateURL.as_view(), name='activate'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name='products_details'),
    path('__debug__/', include(debug_toolbar.urls)),
]