from django.urls import path

from . import views

urlpatterns = [
    path("register_user/", views.register_user, name="register_user"),
    path(
        "update_user/",
        views.update_user_profile,
        name="update_user",
    ),
    path("create_blog/", views.create_blog, name="create_blog"),
    path("list_blog/", views.list_blog, name="list_blog"),
    path("update_blog/<int:pk>/", views.update_blog, name="update_blog"),
    path("delete_blog/<int:pk>/", views.delete_blog, name="delete_blog"),
]
