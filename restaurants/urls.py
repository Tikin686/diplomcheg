from restaurants.apps import RestaurantsConfig
from django.urls import path
from restaurants.views import RestaurantDetailView, RestaurantListView, RestaurantCreateView, RestaurantUpdateView, \
    RestaurantDeleteView, ReserveCreateView, ReserveListView, ReserveCancelView, ReserveUpdateView

app_name = RestaurantsConfig.name

urlpatterns = [
    path('', RestaurantListView.as_view(), name='restaurant_list'),
    path('create/', RestaurantCreateView.as_view(), name='restaurant_create'),
    path('<int:pk>/update/', RestaurantUpdateView.as_view(), name='restaurant_update'),
    path('<int:pk>/', RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('<int:pk>/delete/', RestaurantDeleteView.as_view(), name='restaurant_delete'),
    path('<int:pk>/reserve/create/', ReserveCreateView.as_view(), name='reserve_create'),
    path('reserve/', ReserveListView.as_view(), name='reserve_list'),
    path('reserve/<int:pk>/cancel/', ReserveCancelView.as_view(), name='reserve_cancel'),
    path('reserve/<int:pk>/update/', ReserveUpdateView.as_view(), name='reserve_update'),
]