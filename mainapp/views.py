from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from .token import activation_token
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import AuthorProfile
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import *
from shop.models import Category, Product

# -*- coding: utf-8 -*-
# Create your views here.
def index(request):
    all_products = Product.objects.filter(available=True).order_by('-id')[:10]
    category = Category.objects.all()
    # paginator = Paginator(all_products, 10)  # Show 4 content per page
    # page = request.GET.get('page')
    # total_article = paginator.get_page(page)

    context = {
        'all_products': all_products,
        'all_category': category,

    }
    return render(request, 'main_apps/index.html', context)


def mes_service_list(request, location_id=None):
    location = None
    locations = MesLocation.objects.all()
    post = MesService.objects.all().filter(check=True, active=True)
    qq = MesLocation.objects.values("location_name").annotate(Count("messervice"))
    query = request.GET.get('q')
    if query:
        lookups = (Q(mes_name__icontains=query) |
                   Q(description__icontains=query) |
                   Q(mes_category__icontains=query)
                   )
        post = post.filter(lookups)

    if location_id:
        location = get_object_or_404(MesLocation, location_name=location_id)
        post = MesService.objects.filter(location=location.id)

    context = {
        'post': post,
        'locations': locations,
        'location': location,
        'qq': qq

    }
    return render(request, "main_apps/mes_service_list.html", context)


def tuition_service_list(request, category_id=None):  # when clicked category
    category = None
    categories = TuitionServiceSubject.objects.all()
    post = TuitionService.objects.all().filter(check=True, active=True)  # or (category=cat)
    query = request.GET.get('q')
    if query:
        lookups = (Q(salary__icontains=query) |
                   Q(description__icontains=query)
                   )
        post = post.filter(lookups)

    if category_id:
        category = get_object_or_404(TuitionServiceSubject, id=category_id)
        post = TuitionService.objects.filter(category=category.id)

    context = {
        'post': post,
        'categories': categories,
        'category': category,
    }
    return render(request, "main_apps/tuition_service_list.html", context)


def mes_service_details(request, id):
    single_post = get_object_or_404(MesService, id=id)
    # get_comment = Comment.objects.filter(post=id)
    related = MesService.objects.filter(location=single_post.location).exclude(id=id)[:8]

    # if request.method == 'POST':
    #     name = request.POST.get('name')
    #     email = request.POST.get('email')
    #     post_comment = request.POST.get('message')
    #     get_comment.create(post=single_post, name=name, email=email, post_comment=post_comment)
    #     # reverse('mainapp:single-product', kwargs={'id': id})
    #     return HttpResponseRedirect(reverse('mainapp:index'))

    context = {
        'product': single_post,
        # 'comment': get_comment,
        'relatedpost': related,
    }
    return render(request, 'main_apps/mes_service_details.html', context)


def tuition_service_details(request, t_id):
    post = get_object_or_404(TuitionService, id=t_id)
    author = get_object_or_404(AuthorProfile, name=post.ad_author.name)
    tag = post.category.all()

    context = {
        'post': post,
        'author': author,
        'tag': tag
    }
    return render(request, 'main_apps/tuition_service_details.html', context)


def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('mainapp:index')
                else:
                    messages.error(request, "Disable Account")
            else:
                messages.error(request, "Please enter a correct username and password")
    else:
        form = LoginForm()

    return render(request, 'registration/custom_login.html', {'form': form})


def logout_page(request):
    logout(request)
    return redirect('mainapp:index')


def user_registration(request):
    form = registerUser(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.is_active = False
        instance.save()
        site = get_current_site(request)
        mail_subject = 'MBSTU Bazar | Confirmation Message'
        messages = render_to_string('registration/confirm_email.html', {
            'user': instance,
            'domain': site.domain,
            'uid': instance.id,
            'token': activation_token.make_token(instance),
        })
        to_email = form.cleaned_data.get('email')
        to_list = [to_email]
        from_email = settings.EMAIL_HOST_USER
        send_mail(mail_subject, messages, from_email, to_list, fail_silently=True)
        return render(request, 'registration/confirm_email_send.html')
    return render(request, 'registration/user_registration.html', {'form': form})


def active(request, uid, token):
    try:
        user = get_object_or_404(User, pk=uid)
    except Exception:
        raise Http404('No User Found')
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/confirm_email_send_done.html')
    else:
        raise Http404('Invalid activation link')


@login_required
def user_dashboard(request):
    # all information of the profile holder
    # see tuto 19
    u = get_object_or_404(User, id=request.user.id)

    author_profile = AuthorProfile.objects.filter(name=u.id)

    if author_profile:
        author_user = get_object_or_404(AuthorProfile, name=request.user.id)
        post = MesService.objects.filter(ad_author=author_user.id)  # logged in user's  all post
        approved_post = post.filter(check=True).count()
        is_profile = TuitionService.objects.filter(ad_author=author_user.id)
        check_profile = is_profile.filter(check=True)

        context = {
            'post': post,
            'post_count': post.count(),
            'is_profile': is_profile,
            'approved_post': approved_post,
            'user': author_user,
            'check_profile': check_profile,

        }
        return render(request, 'user_profile/user_profile.html', context)

    else:
        form = createAuthor(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.name = u
            instance.save()
            messages.success(request, "your profile is successfully updated")
            return redirect('mainapp:profile')
        return render(request, 'main_apps/create_profile.html', {'form': form})


@login_required
def update_profile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(AuthorProfile, name=request.user.id)

        form = createAuthor(request.POST or None, request.FILES or None, instance=user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.name = user.name
            instance.save()
            messages.success(request, "successfully updated")
            return redirect('mainapp:profile')
        return render(request, 'main_apps/create_profile.html', {'form': form, 'user': user})

    else:
        return redirect('mainapp:login')


def create_mes_ad(request):
    if request.user.is_authenticated:
        u = get_object_or_404(AuthorProfile, name=request.user.id)
        form = createad(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.ad_author = u
            instance.save()
            messages.success(request, "successfully created")
            return redirect('mainapp:profile')

        return render(request, 'main_apps/create_mes_ad.html', {'form': form, })

    else:
        return redirect('mainapp:login')


def update_mes_ad(request, id, user_id):
    try:
        if request.user.is_authenticated:
            u = get_object_or_404(AuthorProfile, name=request.user.id)
            post = get_object_or_404(MesService, id=id, ad_author=user_id)
            form = createad(request.POST or None, request.FILES or None, instance=post)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.ad_author = u
                instance.save()
                messages.success(request, "successfully updated")
                return redirect('mainapp:profile')

            return render(request, 'main_apps/create_mes_ad.html', {'form': form})
        else:
            return redirect('mainapp:login')
    except Exception as e:
        err = '''Sorry you are not author of this post'''
        return render(request, 'error_page/error1.html', {'e': e, 'err': err})


def delete_mes_ad(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(MesService, id=id)
        post.delete()
        messages.success(request, "successfully deleted")
        return redirect('mainapp:profile')

    else:
        return redirect('mainapp:login')


@login_required
def create_tuition_ad(request):
    u = get_object_or_404(AuthorProfile, name=request.user.id)
    form = EducationInfoForm(request.POST or None, request.FILES or None)
    is_profile = TuitionService.objects.filter(ad_author=u.id)
    if not is_profile:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.ad_author = u
            instance.save()
            form.save_m2m()
            return redirect('mainapp:profile')
        return render(request, 'main_apps/create_tution_ad.html', {'form': form})
    else:
        err = '''You can't create more than 1 tuition profile'''
        return render(request, 'error_page/error1.html', {'err': err})


@login_required
def update_tuition_ad(request):
    u = get_object_or_404(AuthorProfile, name=request.user.id)
    post = get_object_or_404(TuitionService, ad_author=u.id)
    form = EducationInfoForm(request.POST or None, request.FILES or None, instance=post)
    try:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.ad_author = u
            instance.save()
            form.save_m2m()
            messages.success(request, "successfully updated")
            return redirect('mainapp:profile')
    except Exception as e:
        err = '''You have already created tuition service profile'''
        return render(request, 'error_page/error1.html', {'e': e, 'err': err})
    return render(request, 'main_apps/create_tution_ad.html', {'form': form})


@login_required
def delete_tuition_ad(request):
    u = get_object_or_404(AuthorProfile, name=request.user.id)
    post = get_object_or_404(TuitionService, ad_author=u.id)
    post.category.clear()
    post.delete()
    messages.success(request, "successfully deleted")
    return redirect('mainapp:profile')


def contact(request):
    return render(request, 'main_apps/contact.html')


'''
def create_education_status(request):
    if request.user.is_authenticated:
        u = get_object_or_404(AuthorProfile, name=request.user.id)
        if request.method == 'POST':
            get_name = request.POST.get('name')
            get_starting = request.POST.get('starting')
            get_ending = request.POST.get('ending')
            get_description = request.POST.get('description')
            get_degree = request.POST.get('degree')

            try:
                # send_mail('my test mail subject', 'banglai-django test mail body', 'shohan.mbstu@gmail.com',
                #           ['shohan.drmc@gmail.com'], fail_silently=False)
                UserEducationStatus.objects.create(name=get_name, starting=get_starting, ending=get_ending,
                                                   description=get_description, user=u, degree=get_degree)
                return HttpResponseRedirect(reverse('mainapp:profile'))
            except Exception as e:
                return render(request, 'error_page/error1.html', {'e': e})

        else:
            raise Http404("Please correction to your form")

        # return HttpResponse("Add Educational Status")

'''

'''
def delete_education_status(request, e_id):
    if request.user.is_authenticated:
        post = get_object_or_404(UserEducationStatus, id=e_id)
        post.delete()
        messages.success(request, "successfully deleted")
        return redirect('mainapp:profile')

    else:
        return redirect('mainapp:login')
'''

'''
def create_tuition_service(request):
    if request.user.is_authenticated:
        u = get_object_or_404(AuthorProfile, name=request.user.id)
        if request.method == 'POST':
            get_classes1 = request.POST.get('classes1')
            get_week1 = request.POST.get('week1')
            get_subject1 = request.POST.get('subject1')
            get_charge1 = request.POST.get('charge1')

            get_classes2 = request.POST.get('classes2')
            get_week2 = request.POST.get('week2')
            get_subject2 = request.POST.get('subject2')
            get_charge2 = request.POST.get('charge2')

            try:
                TutionService.objects.create(ad_author=u, subject_1=get_subject1, days_in_week_1=get_week1,
                                             class_1=get_classes1, charge_1=get_charge1, subject_2=get_subject2,
                                             days_in_week_2=get_week2,
                                             class_2=get_classes2, charge_2=get_charge2
                                             )
                return HttpResponseRedirect(reverse('mainapp:index'))
            except Exception as e:
                err = 'This user has already created tution ad'
                return render(request, 'error_page/error1.html', {'e': e, 'err': err})
                # raise Http404("Already created this user")

        else:
            raise Http404("Please correction to your form")
'''

'''
def search(request):
    all_products = Product.objects.all()
    query = request.GET.get('q')
    if query:
        lookups = (Q(name__icontains=query) |
                   Q(description__icontains=query)
                   )
        all_products = all_products.filter(lookups)

    context = {
        'products': all_products,
    }
    return render(request, 'main_apps/search.html', context)
'''
