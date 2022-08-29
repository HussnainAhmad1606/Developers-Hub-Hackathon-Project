from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="homepage"),
    path('developers/', views.developers, name="developers"),
    path('search/', views.searchDev, name="searchDev"),
    path('developers/add/', views.add_developer, name="add_developer"),
    path('developers/delete/<str:pk>', views.delete_developer, name="delete_developer"),
    path('developers/update/<str:pk>', views.update_developer, name="update_developer"),
    path('developers/profile/<str:pk>/', views.dev_profile, name="dev_profile"),
    path('login/', views.handleLogin, name="login"),
    path('signup/', views.handleSignup, name="signup"),
    path('logout/', views.handlelogout, name="logout"),

]
