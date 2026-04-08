from django.contrib import admin
from faculty.models import StudentDetails, BookDetails, BookReservation

# Register your models here.
admin.site.register(StudentDetails)
admin.site.register(BookDetails)
admin.site.register(BookReservation)
