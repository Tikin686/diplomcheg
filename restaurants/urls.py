from restaurants.apps import RestaurantsConfig
from django.urls import path
from restaurants.views import RestaurantDetailView, RestaurantListView, RestaurantCreateView, RestaurantUpdateView, RestaurantDeleteView, index


app_name = RestaurantsConfig.name

urlpatterns = [
    path('', RestaurantListView.as_view(), name='restaurant_list'),
    path('create/', RestaurantCreateView.as_view(), name='restaurant_create'),
    path('<int:pk>/update/', RestaurantUpdateView.as_view(), name='restaurant_update'),
    path('<int:pk>/', RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('<int:pk>/delete/', RestaurantDeleteView.as_view(), name='restaurant_delete')
]