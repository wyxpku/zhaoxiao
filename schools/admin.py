from django.contrib import admin
from schools.models import School
from schools.models import Review

# Register your models here.

class SchoolAdmin(admin.ModelAdmin):
	"""docstring for SchoolAdmin"""
	list_display = ('id', 'name', 'administration_dept', 'location', 'level')

class ReviewAdmin(admin.ModelAdmin):
	"""docstring for ReviewAdmin"""
	list_display = ('id', 'school', 'overall_rating', 'review_date')
		
		
admin.site.register(School, SchoolAdmin)
admin.site.register(Review, ReviewAdmin)
