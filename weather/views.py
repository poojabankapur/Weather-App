import requests
from django.shortcuts import render, redirect

# Create your views here.
from weather.forms import CityForm
from weather.models import City


def index(request):
    weather_api_key = '71e370a15531a148e3a11194e19b4086'
    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            newly_added_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=newly_added_city).count()
            url = "https://api.openweathermap.org/data/2.5/weather?q=" + newly_added_city + "&units=imperial&appid=" + weather_api_key

            if existing_city_count == 0:
                r = requests.get(url, format(newly_added_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Invalid city name!'
            else:
                err_msg = 'City already exists!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully'
            message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()
    weather_data = []

    for city in cities:
        url = "https://api.openweathermap.org/data/2.5/weather?q=" + city.name + "&units=imperial&appid=" + weather_api_key
        r = requests.get(url, format(city)).json()
        print(r)
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class
    }
    return render(request, 'weather/weather.html', context)


def delete_city(request, city_name):
    city_to_delete = City.objects.get(name=city_name)
    city_to_delete.delete()
    return redirect('home')
