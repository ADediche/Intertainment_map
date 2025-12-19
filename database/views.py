import json

from django.views.generic import ListView

from .models import Place, PlaceSerializer


class PlaceList(ListView):
    model = Place
    template_name = 'place_list.html'
    context_object_name = 'place_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # generates a JSON object 'Place' with nested images и coordinates
        places = Place.objects.all().prefetch_related('images', 'coordinates')
        serializer = PlaceSerializer(places, many=True)
        context['places_json'] = json.dumps(serializer.data)
        return context
