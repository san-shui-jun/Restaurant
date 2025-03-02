from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404  # , render
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.edit import CreateView
from .models import RestaurantReview, Restaurant, Dish
from .forms import RestaurantForm, DishForm


class RestaurantList(ListView):
    queryset = Restaurant.objects.all().order_by("-date")
    context_object_name = 'latest_restaurant_list'
    telephone_name = 'myrestaurants/restaurant_list.html'


class RestaurantDetail(DetailView):
    model = Restaurant
    template_name = 'myrestaurants/restaurant_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RestaurantDetail, self).get_context_data(**kwargs)
        context['RATING_CHOICES'] = RestaurantReview.RATING_CHOICES
        return context


class RestaurantCreate(CreateView):
    model = Restaurant
    template_name = 'myrestaurants/form.html'
    form_class = RestaurantForm

    def form_valid(self, form):
        '''form_valid方法作用是添加前端表单字段以外的信息。在用户在创建餐厅时，我们不希望用户能更改创建用户，
        于是在前端表单里把user故意除外了(见forms.py)，而选择在后台添加user信息。'''
        form.instance.user = self.request.user
        return super(RestaurantCreate, self).form_valid(form)


class RestaurantEdit(UpdateView):
    model = Restaurant
    template_name = 'myrestaurants/form.html'
    form_class = RestaurantForm


class DishDetail(DetailView):
    model = Dish
    template_name = 'myrestaurants/dish_detail.html'


class DishCreate(CreateView):
    model = Dish
    template_name = 'myrestaurants/form.html'
    form_class = DishForm

    # Associate form.instance.user with self.request.user and get pk value.
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.restaurant = Restaurant.objects.get(id=self.kwargs['pk'])
        return super(DishCreate, self).form_valid(form)


class DishEdit(UpdateView):
    model = Dish
    template_name = 'myrestaurants/form.html'
    form_class = DishForm


def review_create(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    review = RestaurantReview(
        rating=request.POST['rating'],
        comment=request.POST['comment'],
        user=request.user,
        restaurant=restaurant)
    review.save()
    return HttpResponseRedirect(
        reverse('myrestaurants:restaurant_detail', args=[pk]))
