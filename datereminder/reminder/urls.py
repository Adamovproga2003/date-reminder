from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutView, name="logout"),
    path("create/", views.create, name="create"),
    path("add/", views.add, name="add"),
    path("change/<int:person_id>/", views.change, name="change"),
    path("auth/", views.auth, name="auth"),
    path("edit/<int:person_id>/", views.edit, name='edit'),
    path("delete/<int:person_id>/", views.delete, name='delete'),
    path("user/", views.user, name='user')
]
