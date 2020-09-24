from . import views

from django.urls import path


urlpatterns = [
    path('auth', views.AuthAPIView.as_view()),
    path('auth/callback', views.AuthCallbackAPIView.as_view()),
    path('api/artists', views.ArtistReleasesAPIView.as_view())
]
