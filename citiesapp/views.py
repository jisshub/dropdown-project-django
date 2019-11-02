from django.shortcuts import render, redirect
from django.forms import ModelForm
from .models import Person, City, Country


# Create your views here.
class NewForm(ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'birthdate', 'country', 'city')

    # here v override the default init method and then set the
    # queryset of city field to an empty list of cities.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')


def person_create(request, template_name='citiesapp/index.html'):
    form = NewForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, template_name, {'form': form})


# next create a view to return a list of citiesfor a given country
def load_cities(request,
                template_name='citiesapp/dropdown.html'):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, template_name, {'form': cities})
