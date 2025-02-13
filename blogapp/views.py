from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Blog
from .serializers import (
    BlogSerializer,
    UpdateUserSerializer,
    UserRegistrationSerializer,
)


@api_view(["POST"])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def update_user_profile(request):
    user = request.user
    data = request.data.copy()

    # Uzupełnienie brakujących pól aktualnymi wartościami użytkownika
    for field in UpdateUserSerializer().fields:
        if field not in data:
            data[field] = getattr(user, field, None)

    serializer = UpdateUserSerializer(user, data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_blog(request):
    user = request.user
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def list_blog(request):
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_blog(request, pk):
    user = request.user
    blog = get_object_or_404(Blog, pk=pk)
    if blog.author != user:
        return Response(
            {"error": "You are not the author of this blog"},
            status=status.HTTP_403_FORBIDDEN,
        )
    serializer = BlogSerializer(blog, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_blog(request, pk):
    user = request.user
    blog = get_object_or_404(Blog, pk=pk)
    if blog.author != user:
        return Response(
            {"error": "You are not the author of this blog"},
            status=status.HTTP_403_FORBIDDEN,
        )
    blog.delete()
    return Response(
        {"message": "Blog deleted successfully"},
        status=status.HTTP_204_NO_CONTENT,
    )
