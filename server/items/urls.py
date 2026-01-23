from django.urls import path
from .views import (
    ItemListCreateView,
    ItemDetailView,
    UserItemsView,
    LikeToggleView,
    UserLikedItemsView,
)

urlpatterns = [
    path("", ItemListCreateView.as_view(), name="item-list-create"),
    path("<int:pk>/", ItemDetailView.as_view(), name="item-detail"),
    path("my-items/", UserItemsView.as_view(), name="user-items"),
    path("<int:item_id>/like/", LikeToggleView.as_view(), name="like-toggle"),
    path("liked/", UserLikedItemsView.as_view(), name="user-liked-items"),
]
