from django.contrib import admin
from .models import Event, Wishlist, TShirt, AboutCollege, AboutPreviousVitopia, BookedEvent,Sport

admin.site.register(Event)
admin.site.register(Wishlist)  # ✅ Fix: Register Wishlist model
admin.site.register(TShirt)
admin.site.register(AboutCollege)
admin.site.register(AboutPreviousVitopia)
admin.site.register(BookedEvent) 
admin.site.register(Sport) # ✅ Fix: Register BookedEvent model
