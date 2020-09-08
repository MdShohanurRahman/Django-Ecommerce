from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from mainapp.models import AuthorProfile


# class Category(models.Model):
#     name = models.CharField(max_length=150, db_index=True)
#     slug = models.SlugField(max_length=150, unique=True, db_index=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ('name',)
#         verbose_name = 'category'
#         verbose_name_plural = 'categories'
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('shop:product_list_by_category', args=[self.slug])

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        unique_together = ('slug', 'parent',)  # enforcing that there can not be two
        verbose_name_plural = "categories"  # categories under a parent with same
        # slug

    def __str__(self):  # __str__ method elaborated later in
        full_path = [self.name]  # post.  use __unicode__ in place of
        # __str__ if you are using python 2
        k = self.parent

        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = RichTextUploadingField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    past_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    brand_new = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    post_comment = models.TextField()
    posted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.post.name  # cause foreign key


class BookOrder(models.Model):
    book_name = models.CharField(max_length=50)
    author_name = models.CharField(max_length=50)
    edition = models.CharField(max_length=20)
    quantity = models.IntegerField(blank=True, null=True)
    contact = models.CharField(max_length=11)

    def __str__(self):
        return self.book_name


class Post(models.Model):
    user = models.CharField(max_length=120)
    title = models.CharField(max_length=120)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=120)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False, )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def get_cat_list(self):  # for now ignore this instance method,
        k = self.category
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent

        for i in range(len(breadcrumb) - 1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i - 1:-1])
        return breadcrumb[-1:0:-1]
