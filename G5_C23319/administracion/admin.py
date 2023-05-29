from django.contrib import admin


from .models import NaturalPark
from .models import Category
from .models import Campsite
from .models import Availability
from .models import Reservation
from .models import Profile

admin.site.register(NaturalPark)
admin.site.register(Category)
admin.site.register(Campsite)
admin.site.register(Availability)
admin.site.register(Reservation)
admin.site.register(Profile)
