import debug_toolbar
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="shop/password_reset.html"), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="shop/password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="shop/password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="shop/password_reset_done.html"), name ='password_reset_complete'),
    # path('', include('django.contrib.auth.urls')),
    path('categories/', views.cat.as_view(), name='category'),
    path('categories/<slug:pk>', views.catDetails.as_view(), name='category'),
    path('signup/', views.Signup.as_view(), name="signup"),
    path('activate/<uidb>/<token>/', views.ActivateURL.as_view(), name='activate'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name='products_details'),
    path('__debug__/', include(debug_toolbar.urls)),
]