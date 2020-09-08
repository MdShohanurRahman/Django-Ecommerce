from ckeditor_uploader.fields import RichTextUploadingField
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField

# Create your models here.
from django.urls import reverse


class AuthorProfile(models.Model):
    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHERS', 'Others'),
    )

    name = models.OneToOneField(User, on_delete=models.CASCADE)  # one to one field
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    profile_picture = models.ImageField(upload_to='author_profile/%Y/%m/%d')
    Date_Of_Birth = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    present_address = models.CharField(max_length=200)
    contact = models.CharField(max_length=11)
    facebook_id = models.URLField(max_length=300, blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    check = models.BooleanField(default=False)

    def __str__(self):
        return self.name.username


class MesLocation(models.Model):
    location_name = models.CharField(max_length=100)

    class Meta:
        ordering = ('location_name',)

    def __str__(self):
        return self.location_name

    def get_absolute_url(self):
        return reverse('mainapp:mes_list_by_category', args=[self.location_name])


class MesService(models.Model):
    MES_CATEGORY = (
        ('boys', 'Boys-Mes'),
        ('girls', 'Girls-Mes'),
    )

    ad_author = models.ForeignKey(AuthorProfile, on_delete=models.CASCADE)
    mes_name = models.CharField(max_length=100)
    location = models.ForeignKey(MesLocation, on_delete=models.CASCADE)
    mes_category = models.CharField(max_length=10, choices=MES_CATEGORY, blank=True)
    title = models.CharField(max_length=200)
    # image = models.ImageField(upload_to='mes_service/%Y/%m/%d', blank=True)
    # description = models.TextField()
    # description = RichTextField()
    description = RichTextUploadingField()
    seat_rent = models.DecimalField(max_digits=10, decimal_places=2)
    posted_on = models.DateField(auto_now=False, auto_now_add=True)
    updated_on = models.DateField(auto_now=True, auto_now_add=False)
    check = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    # class Meta:
    #     ordering =['-id']

    def __str__(self):
        return self.mes_name

    def get_absolute_url(self):
        return reverse('mainapp:mes_details', args=[self.id])


class TuitionServiceSubject(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


class TuitionService(models.Model):
    SEMESTER_CHOICES = (
        ('1st Year 1st Semester', '1st Year 1st Semester'),
        ('1st Year 2nd Semester', '1st Year 2nd Semester'),
        ('2nd Year 1st Semester', '2nd Year 1st Semester'),
        ('2nd Year 2nd Semester', '2nd Year 2nd Semester'),
        ('3rd Year 1st Semester', '3rd Year 1st Semester'),
        ('3rd Year 2nd Semester', '3rd Year 2nd Semester'),
        ('4th Year 1st Semester', '4th Year 1st Semester'),
        ('4th Year 2nd Semester', '4th Year 2nd Semester'),
    )

    DEPARTMENT_CHOICES = (
        ('ICT', 'ICT'),
        ('CSE', 'CSE'),
        ('TEXTILE', 'TEXTILE'),
        ('ESRM', 'ESRM'),
        ('CPS', 'CPS'),
        ('FTNS', 'FTNS'),
        ('BGE', 'BGE'),
        ('PHARMACY', 'PHARMACY'),
        ('BMB', 'BMB'),
        ('BBA', 'BBA'),
        ('CHEMISTRY', 'CHEMISTRY'),
        ('PHYSICS', 'PHYSICS'),
        ('MATHEMATICS', 'MATHEMATICS'),
        ('STATISTICS', 'STATISTICS'),
        ('ECONOMICS', 'ECONOMICS'),

    )

    DAY_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    )
    gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    ad_author = models.OneToOneField(AuthorProfile, on_delete=models.CASCADE)
    category = models.ManyToManyField(TuitionServiceSubject, related_name='category_tag', blank=True)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    student_id = models.CharField(max_length=10, unique=True)
    semester = models.CharField(max_length=30, choices=SEMESTER_CHOICES)
    days_in_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    description = RichTextUploadingField()
    posted_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    check = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{}'s Tuition Plan ".format(self.ad_author.name.username)

    def get_absolute_url(self):
        return reverse('mainapp:tuition_details', args=[self.id])


'''
class Comment(models.Model):
    post = models.ForeignKey(MesService, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    post_comment = models.TextField()
    posted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.post.title  # cause foreign key


class UserEducationStatus(models.Model):
    user = models.ForeignKey(AuthorProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    starting = models.DateField()
    ending = models.DateField(blank=True, null=True, )
    description = models.TextField(max_length=200)

    def __str__(self):
        return "{} Education Details of {}".format(self.user.id, self.user.name.username)
'''

'''
class MesCategory(models.Model):
    category_name = models.CharField(max_length=100)

    class Meta:
        ordering = ('category_name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
'''
