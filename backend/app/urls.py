from django.urls import path

from . import views


urlpatterns = [
    path('family-tree/<str:identity_number>/lineage/', views.PersonFamilyTreeListView.as_view(), name='api-family-tree'),
]
