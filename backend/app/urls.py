from django.urls import path

from . import views

urlpatterns = [
    path(
        "family-tree/<str:identity_number>/lineage/",
        views.PersonFamilyTreeListView.as_view(),
        name="api-family-tree",
    ),
    path(
        "root-ascendant/<str:identity_number>/",
        views.PersonRootAscendantView.as_view(),
        name="api-root-ascendant",
    ),
]
