from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item, Like
from .serializers import ItemSerializer


class ItemListCreateView(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        search = self.request.query_params.get("search", "")
        if search:
            from django.db.models import Q

            return Item.objects.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        return Item.objects.all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # FLAW 1: A01 - Broken Access Control
    # Any authenticated user can update or delete any item, even if they don't own it.
    def perform_destroy(self, instance):
        instance.delete()

    def perform_update(self, serializer):
        serializer.save()

    # FIX:
    # move next line up to imports:
    # from rest_framework.exceptions import PermissionDenied

    # def perform_destroy(self, instance):
    #     if instance.seller != self.request.user:
    #         raise PermissionDenied("You don't have permission to delete this item.")
    #     instance.delete()

    # def perform_update(self, serializer):
    #     if serializer.instance.seller != self.request.user:
    #         raise PermissionDenied("You don't have permission to edit this item.")
    #     serializer.save()


class UserItemsView(generics.ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Item.objects.filter(seller=self.request.user)


class LikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response(
                {"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND
            )

        like, created = Like.objects.get_or_create(user=request.user, item=item)

        if not created:
            like.delete()
            return Response({"liked": False}, status=status.HTTP_200_OK)

        return Response({"liked": True}, status=status.HTTP_201_CREATED)


class UserLikedItemsView(generics.ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        liked_items_ids = Like.objects.filter(user=self.request.user).values_list(
            "item_id", flat=True
        )
        return Item.objects.filter(id__in=liked_items_ids)
