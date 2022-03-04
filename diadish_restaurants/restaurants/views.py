from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .utils import get_ip_address
from .models import Restaurants, Menu
from geopy.distance import geodesic
import requests
import logging

logger = logging.getLogger(__name__)

# Create your views here.

def home_page(request, latitude=None, longitude=None, param='default'):
    """
    Analyse request data and returns the restaurants list on the basis of user's location and filter option

    param: 
        request: request data from user
        latitude: latitude entered by user (by default None)
        longitude: longitude entered by user (by default None)
        param: sort/filter parameter (by default default)
    return:
        renders: request, templates url, context body to be displayed

    """

    logger.debug(param)

    location_from_user = []

    if param == 'default':
        '''
            since location in the form of latitude and longitude not entered by user
            calling get_ip_address function for fetching IP address of user
            filter param is also default
            setting value of param to all_type
        '''
        param = 'all_type'
        user_ip_address = get_ip_address(request)

        ip_api_url = "http://ip-api.com/batch"

        json = [
            {"query": user_ip_address},
        ]

        '''
            calling ip_api_url for getting the latitude and longitude of user 
            on the basis of ip address
        '''
        response = requests.request(method="post", url=ip_api_url, json=json)
        response = response.json()
        logger.debug(response)

        if response[0]['status'] == 'success':
            logger.debug(response)
            user_latitude = response[0]['lat']
            user_longitude = response[0]['lon']
            logger.debug("user's ip address latitude {}".format(user_latitude))
            logger.debug("user's ip address longitude {}".format(user_longitude))
            location_from_user = (user_latitude, user_longitude)
        else:
            logger.debug("Failed to get latitude and longitude from ip address")
    else:
        '''
            location in the form of latitude and longitude entered by user
        '''
        logger.debug("latitude entered by user is {}".format(latitude))
        logger.debug("longitude entered by user is {}".format(longitude))
        logger.debug("filter parameter entered by user is {}".format(param))

        location_from_user = (latitude, longitude)

    restaurants_queryset = []
    try:
        if param == 'rating':
            restaurants_queryset = Restaurants.objects.order_by('-rating')
        elif param == 'price':
            restaurants_queryset = Restaurants.objects.order_by('average_price')
        elif param == 'veg':
            restaurants_queryset = Restaurants.objects.filter(menu__veg=True)
        elif param == 'pizza':
            restaurants_queryset = Restaurants.objects.filter(menu__pizza=True)
        elif param == 'momo':
            restaurants_queryset = Restaurants.objects.filter(menu__momo=True)
        elif param == 'sweets':
            restaurants_queryset = Restaurants.objects.filter(menu__sweets=True)
        elif param == 'south':
            restaurants_queryset = Restaurants.objects.filter(menu__south_indian=True)
        else:
            restaurants_queryset = Restaurants.objects.all()
    except Exception as e:
        logger.debug(e)
        restaurants_queryset = Restaurants.objects.all()

    logger.debug("location_from_user {}".format(location_from_user))
    restaurants_list = []
    for restaurant in restaurants_queryset:
        try:
            restaurant_location = (restaurant.latitude, restaurant.longitude)
            distance = round(geodesic(location_from_user, restaurant_location).km, 2)
            average_cost = restaurant.average_price
            rating = restaurant.rating
            restaurants_list.append([restaurant, distance, rating, average_cost])
        except Exception as e:
            logger.debug(e)

    if param != 'rating' and param != 'price':
        restaurants_list = sorted(restaurants_list, key = lambda k:(k[1],-k[2],k[3]))

    filtered_restaurant_list = []
    for restaurant in restaurants_list:
        try:
            name = restaurant[0].name
            address = restaurant[0].address
            website = restaurant[0].website
            distance = restaurant[1]
            rating = restaurant[2]
            average_cost = restaurant[3]
            free_delivery = 1 if restaurant[0].free_delivery else 0
            restaurant_dict = {
                'name': name,
                'address': address,
                'website': website,
                'rating': rating,
                'distance': distance,
                'average_cost': average_cost,
                'free_delivery': free_delivery
            }
            filtered_restaurant_list.append(restaurant_dict)
        except Exception as e:
            logger.debug(e)

    logger.debug("restaurants list to be returned")
    logger.debug(filtered_restaurant_list)

    context = {
        'restaurants_list': filtered_restaurant_list
    }
    return render(request, 'restaurants/home.html', context)