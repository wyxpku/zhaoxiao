from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from schools.models import School, Review
from django.core import serializers
from django.db.models import Avg


import jieba

# 主页面
def index(request):
    return render(request, 'index.html')

# 搜索结果页面
def search(request):
    querystr = request.GET['q']
    # return HttpResponse(querystr)

    keywords = [str(item) for item in jieba.cut(querystr, cut_all=False)]
    keywords.sort(key=lambda x: -len(x))
    print(keywords)
    search_result = []
    schools = School.objects.all().order_by('id')

    for keyword in keywords:
        print("keyword:", keyword)
        for school in schools:
            if keyword in school.name:
                if not school in search_result:
                    search_result.append(school)

    return render(
        request,
        'searchresult.html',
        {
            'query': querystr,
            "result_num": len(search_result),
            "schools": search_result,
        }
    )

def get_school_info(id):
    try:
        school = School.objects.get(id=id)
        reviews = Review.objects.filter(school=school)
        info = {'review_num': len(reviews)}
        info.update(reviews.aggregate(Avg('overall_rating')))
        info.update(reviews.aggregate(Avg('academic_rating')))
        info.update(reviews.aggregate(Avg('campus_rating')))
        info.update(reviews.aggregate(Avg('dining_rating')))
        info.update(reviews.aggregate(Avg('dorm_rating')))

        info.update(reviews.aggregate(Avg('administration_rating')))
        info.update(reviews.aggregate(Avg('facility_rating')))
        info.update(reviews.aggregate(Avg('organization_rating')))
        info.update(reviews.aggregate(Avg('location_rating')))

        # info = {
        #     'review_num': len(reviews),
        #     'overall_rating': reviews.aggregate(Avg('overall_rating'))['overall_rating__avg'],
        #     'academic_rating': reviews.aggregate(Avg('academic_rating')),
        #     'campus_rating': reviews.aggregate(Avg('campus_rating')),
        #     'dining_rating': reviews.aggregate(Avg('dining_rating')),
        #     'dorm_rating': reviews.aggregate(Avg('dorm_rating')),
        #     'administration_rating': reviews.aggregate(Avg('administration_rating')),
        #     'facility_rating': reviews.aggregate(Avg('facility_rating')),
        #     'organization_rating': reviews.aggregate(Avg('organization_rating')),
        #     'location_rating': reviews.aggregate(Avg('location_rating')),
        # }
        return info
    except Exception as e:
        print(e)
        return None

def get_level(rate):
    print(type(rate))
    if rate >= 4.5:
        return 'A+'
    if rate >= 4.0:
        return 'A'
    if rate >= 3.5:
        return 'B+'
    if rate >= 3.0:
        return 'B'
    if rate >= 2.5:
        return 'C+'
    if rate >= 2.0:
        return 'C'
    if rate >= 1.5:
        return 'D+'
    if rate >= 1.0:
        return 'D'
    if rate >= '0.5':
        return 'E+'
    if rate > '0':
        return 'E'
    return 'N'

# 学校详情页面
def school_detail(request, id):
    try:
        school = School.objects.get(id=id)
        info = get_school_info(id)
        preinfo = info.copy()
        for k, v in preinfo.items():
            if k == 'review_num':
                continue
            info[k + '_level'] = get_level(v)
        print(info)
    except Exception as e:
        print(e)
        retdata = {
            'status': False,
            'info': str(e),
        }
        return render(request, 'school.html', {'school': None})

    if request.method == 'GET':
        # serializer = SchoolSerializer(school)
        # retdata = serializer.data
        # retdata['status'] = True
        return render(request, 'school.html', {'school': school, 'school_info': info})

# 评论页面
def review(request, id):
    if request.method == 'GET':
        try:
            school = School.objects.get(id=id)
        except Exception as e:
            retdata = {
                'status': False,
                'info': str(e),
            }
            return render(request, 'school.html', {'school': None})

        return render(request, 'review.html', {'school': school})
    elif request.method == 'POST':
        print(request.POST)
        newreview = Review()
        try:
            newreview.overall_rating = request.POST['overall_rating']
            newreview.academic_rating = request.POST['academic_rating']
            newreview.campus_rating = request.POST['campus_rating']
            newreview.dining_rating = request.POST['dining_rating']
            newreview.dorm_rating = request.POST['dorm_rating']
            newreview.administration_rating = request.POST['administration_rating']
            newreview.facility_rating = request.POST['facility_rating']
            newreview.organization_rating = request.POST['organization_rating']
            newreview.location_rating = request.POST['location_rating']
            newreview.facility_rating = request.POST['facility_rating']
            newreview.reviewer_relationship = request.POST['reviewer_relationship']
            newreview.reviewer_major = request.POST['reviewer_major']
            newreview.review_content = request.POST['review_content']

            school = School.objects.get(id=id)
            newreview.school = school
            newreview.full_clean()
            newreview.save()
        except Exception as e:
            print(e)
            return HttpResponse("Error saving review")
        return redirect(school.get_absolute_url())

# 搜索建议


def autocomplete(request):
    prefix = request.GET['q']
    search_result = []
    schools = School.objects.all().order_by('id')
    for school in schools:
        if school.name.startswith(prefix):
            search_result.append(school)
    search_result.sort(key=lambda x: len(x.name))
    retdata = serializers.serialize('json', search_result)
    # retdata['len'] = len(search_result)
    return HttpResponse(retdata, content_type='application/json')
