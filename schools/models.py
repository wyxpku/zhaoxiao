from django.db import models

# Create your models here.


class School(models.Model):
    name = models.CharField(max_length=128)
    administration_dept = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    level = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/school/%i/" % self.id


class Review(models.Model):
    RATING_CHOICES = (
        (1, u'很好'),
        (2, u'好'),
        (3, u'中等'),
        (4, u'差'),
        (5, u'很差'),
    )
    RELATIONSHIP_CHOICES = (
        (1, u'大一学生'),
        (2, u'大二学生'),
        (3, u'大三学生'),
        (4, u'大四学生'),
        (5, u'研究生/博士生'),
        (6, u'校友'),
        (7, u'教职工'),
        (8, u'其他'),
    )
    overall_rating = models.IntegerField(choices=RATING_CHOICES)
    academic_rating = models.IntegerField(choices=RATING_CHOICES)
    campus_rating = models.IntegerField(choices=RATING_CHOICES)
    dining_rating = models.IntegerField(choices=RATING_CHOICES)
    dorm_rating = models.IntegerField(choices=RATING_CHOICES)
    administration_rating = models.IntegerField(choices=RATING_CHOICES)
    facility_rating = models.IntegerField(choices=RATING_CHOICES)
    organization_rating = models.IntegerField(choices=RATING_CHOICES)
    location_rating = models.IntegerField(choices=RATING_CHOICES)
    reviewer_relationship = models.IntegerField(choices=RELATIONSHIP_CHOICES)
    reviewer_major = models.CharField(max_length=64)
    reviewer_date = models.DateTimeField(auto_now_add=True)

    review_content = models.TextField()
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.id)
