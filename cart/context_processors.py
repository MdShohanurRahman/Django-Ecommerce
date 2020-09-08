from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect

from .cart import Cart
from mainapp.models import AuthorProfile


def cart(request):
    return {'cart': Cart(request)}


def user(request):
    global author_user
    if request.user.is_authenticated:
        u = get_object_or_404(User, id=request.user.id)
        author_profile = AuthorProfile.objects.filter(name=u.id)
        if author_profile:
            author_user = get_object_or_404(AuthorProfile, name=request.user.id)
            return {'author_user': author_user}
    else:
        u = User.objects.get(id=1)
        author_profile = AuthorProfile.objects.filter(name=u.id)
        if author_profile:
            author_user = get_object_or_404(AuthorProfile, name=request.user.id)
            return {'author_user': author_user}
