from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Restaurant(models.Model):
    name = models.TextField()
    address = models.TextField(blank=True, default='')
    telephone = models.TextField(blank=True, default='')
    url = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        '''定义一个get_absolute_url()方法来告诉Django如何计算对象的规范URL。
        对于调用者，此方法应该看起来像返回一个字符串，该字符串可用于通过HTTP引用该对象。'''
        return reverse('myrestaurants:restaurant_detail', args=[str(self.id)])


class Dish(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    '''DecimalField.max_digits数字中允许的最大位数。请注意，此数字必须大于或等于decimal_places。
    DecimalField.decimal_places与数字一起存储的小数位数。'''
    price = models.DecimalField('USD amount', max_digits=8, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    #  FileField.upload_to此属性提供了一种设置上传目录和文件名的方法,文件保存在media/myrestaurants/目录下
    image = models.ImageField(upload_to='myrestaurants', blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, null=True, related_name='dishes', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('myrestaurants:dish_detail', args=[str(self.restaurant.id), str(self.id)])


class Review(models.Model):
    RATING_CHOICES = ((1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five'))
    rating = models.PositiveSmallIntegerField('Rating(stars)', blank=False, default=3, choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    class Meta:
        '''抽象基类，如果你需要将一些公共信息放在许多模型中，可以在Meta选项中设置abstract = True
        表示作为一个基类，可以被继承，但是此类不会生成数据库，仅作为一个类对Meta的继承，
        当你在继承抽象基类的时候，如果子类没有声明Meta类，将继承父类的Meta类,也可以自己定义'''
        abstract = True


class RestaurantReview(Review):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return "{} review".format(self.restaurant.name)
