from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item, Like
from .serializers import ItemSerializer


# FLAW 3: A05 - SQL Injection
# Using raw SQL without parameterization allows SQL injection attacks
# Using executescript() allows multiple SQL statements
# User can write this in search bar to change prices: '; UPDATE items_item SET price=0 WHERE id=1; --
class ItemListCreateView(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        search = self.request.query_params.get("search", "")

        if search:
            from django.db import connection

            query = f"""
                SELECT * FROM items_item 
                WHERE title LIKE '%{search}%' 
                OR description LIKE '%{search}%';
            """

            cursor = connection.cursor()
            cursor.db.connection.executescript(query)

            cursor.execute("SELECT * FROM items_item")
            columns = [col[0] for col in cursor.description]
            results = []
            for row in cursor.fetchall():
                item_dict = dict(zip(columns, row))
                results.append(Item(**item_dict))
            return results

        return Item.objects.all()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


# FIX: Use Django ORM with proper filtering:
# class ItemListCreateView(generics.ListCreateAPIView):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ["title", "description"]
#
#     def perform_create(self, serializer):
#         serializer.save(seller=self.request.user)


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
