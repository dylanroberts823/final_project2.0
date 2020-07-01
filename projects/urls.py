from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("create/", views.create_view, name="create"),
    path("manage/", views.manage_view, name="manage"),
    path("manage/<int:project_id>/", views.manage_project_view, name="manage_project"),
    path("manage/<int:project_id>/modify_project", views.modify_project_view, name="modify_project"),
    path("request/<int:project_id>/", views.request_view, name="request"),
    path("myrequests/", views.myrequests_view, name="myrequests"),
    path("approve/<int:request_id>", views.approve_view, name="approve"),
    path("deny/<int:request_id>", views.deny_view, name="deny"),
    path("<int:request_id>/<int:modification_id>/modify/", views.request_modification_view, name="request_modification"),
    path("create_tag/", views.create_tag_view, name="create_tag"),
]
