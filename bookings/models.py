from django.db import models
from django.contrib.auth.models import User

# ✅ Event Model
class Event(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/')
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    ticket_count = models.PositiveIntegerField(default=0)  # ✅ Ensure default value
    time = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.name

# ✅ Wishlist Model (Prevent Duplicate Entries)
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'event')  # ✅ Prevent duplicates

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"

# ✅ T-Shirt Model
class TShirt(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='tshirts/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_date = models.DateTimeField(auto_now=True)  # ✅ Fixed tracking issue

    def __str__(self):
        return self.name

# ✅ About College Model
class AboutCollege(models.Model):
    image = models.ImageField(upload_to='about_college/')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return "About College"

# ✅ About Previous Vitopia Model
class AboutPreviousVitopia(models.Model):
    image = models.ImageField(upload_to='about_previous/')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return "About Previous Vitopia"

class BookedEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255, unique=True, null=True, blank=True)  # ✅ Allow empty values
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booked - {self.user.username} - {self.event.name}"

class Sport(models.Model):
    name = models.CharField(max_length=255, default="Unknown Sport", unique=True, verbose_name="Sport Name")
    image = models.ImageField(upload_to='sports_images/', default='sports_images/default_sport.jpg')
    joining_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Joining Fee")
    winning_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Winning Prize")

    class Meta:
        verbose_name = "Sport"
        verbose_name_plural = "Sports"

    def __str__(self):
        return f"{self.name} - Joining: ₹{self.joining_price}, Winning: ₹{self.winning_price}"
