from django.shortcuts import render, redirect
from django.http import HttpResponse
from schools.models import School, Review
from django.core import serializers
from django.db.models import Avg
import math

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
    # print(keywords)
    search_result = []
    schools = School.objects.all().order_by('id')

    for keyword in keywords:
        # print("keyword:", keyword)
        for school in schools:
            if keyword in school.name:
                if school not in search_result:
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

        info['stars'] = [
            len(reviews.filter(overall_rating=i)) for i in range(1, 6)
        ]
        if len(reviews) == 0:
            info['stars_p'] = [0 for i in range(5)]
        else:
            info['stars_p'] = [
                item / len(reviews) * 100 for item in info['stars']
            ]
        return info
    except Exception as e:
        print(e)
        return None


def get_level(rate):
    # print(type(rate))
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
    if rate >= 0.5:
        return 'E+'
    if rate > 0:
        return 'E'
    return 'N'


# 学校详情页面
def school_detail(request, id):
    try:
        school = School.objects.get(id=id)
        info = get_school_info(id)
        preinfo = info.copy()
        for k, v in preinfo.items():
            if type(v) is list:
                continue
            if k == 'review_num':
                continue
            if v is None:
                info[k] = 0
                info[k + '_level'] = 'N'
            else:
                info[k + '_level'] = get_level(v)
    except Exception as e:
        print(e)
        return render(request, 'school.html', {'school': None})

    if request.method == 'GET':
        # serializer = SchoolSerializer(school)
        # retdata = serializer.data
        # retdata['status'] = True
        retdata = {
            'school': school,
            'school_info': info,
        }
        return render(request, 'school.html', retdata)


# 评论页面
def review(request, id):
    if request.method == 'GET':
        try:
            school = School.objects.get(id=id)
            info = get_school_info(id)
            preinfo = info.copy()
            for k, v in preinfo.items():
                if type(v) is list:
                    continue
                if k == 'review_num':
                    continue
                if v is None:
                    info[k] = 0
                    info[k + '_level'] = 'N'
                else:
                    info[k + '_level'] = get_level(v)
        except Exception as e:
            print(e)
            return render(request, 'school.html', {'school': None})
        # print(info)
        retdata = {
            'school': school,
            'school_info': info,
        }
        return render(request, 'review.html', retdata)
    elif request.method == 'POST':
        # print(request.POST)
        newreview = Review()
        try:
            newreview.overall_rating = request.POST['overall_rating']
            newreview.academic_rating = request.POST['academic_rating']
            newreview.campus_rating = request.POST['campus_rating']
            newreview.dining_rating = request.POST['dining_rating']
            newreview.dorm_rating = request.POST['dorm_rating']
            newreview.administration_rating =\
                request.POST['administration_rating']
            newreview.facility_rating = request.POST['facility_rating']
            newreview.organization_rating = request.POST['organization_rating']
            newreview.location_rating = request.POST['location_rating']
            newreview.facility_rating = request.POST['facility_rating']
            newreview.reviewer_relationship =\
                request.POST['reviewer_relationship']
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


def getreviews(school, review_filter, review_order):
    reviews = None
    review_filter = int(review_filter)
    if review_filter == 0:
        reviews = Review.objects.filter(school=school)
    else:
        reviews = Review.objects.filter(
            school=school,
            overall_rating=review_filter
        )
    # print(type(review_order))
    if review_order == 1:
        reviews = reviews.order_by('-review_date')
    elif review_order == 2:
        reviews = reviews.order_by('-overall_rating', '-review_date')
    elif review_order == 3:
        reviews = reviews.order_by('reviewer_major', '-review_date')
    # print(type(reviews))
    return reviews


# 加载评论
def reviewsapi(request):
    # print(request.GET)
    if request.method != 'GET':
        return HttpResponse(
            '<h5 style="width: 100%;text-align:center;">Error Http Method</h5>'
        )
    # try:
    school_id = request.GET.get('school', None)
    school = School.objects.get(id=school_id)

    # filter overall_rating
    #   0: all
    #   1: 1 star
    #   2: 2 star
    #   ...
    review_filter = request.GET.get('filter', 0)

    # sort
    #   1. review time
    #   2. overall_rating
    #   3. reviewer major
    review_order = request.GET.get('order', 1)
    # page
    review_page = request.GET.get('page', 1)

    review_page = int(review_page)
    review_order = int(review_order)
    review_filter = int(review_filter)
    
    # print(review_filter, review_order, review_page)
    reviews = getreviews(school, review_filter, review_order)
    perpage = 10
    retdata = {}
    totalnum = len(reviews)
    
    retdata['totalnum'] = totalnum
    retdata['pages'] = math.ceil(totalnum / perpage)
    if int(review_page) > retdata['pages']:
        return HttpResponse('<p style="width: 100%;text-align: center">暂无评论</p>')
    
    retdata['p'] = review_page - 1
    retdata['n'] = review_page + 1
    if review_page == 1:
        retdata['prev'] = 'disabled'
    
    if retdata['pages'] == review_page:
        retdata['reviews'] = reviews[(review_page - 1) * perpage:]
        retdata['next'] = 'disabled'
    else:
        retdata['reviews'] = reviews[(review_page - 1) * perpage: review_page * perpage]

    if review_order == 1:
        retdata['order_info'] = '按评论时间排序：'
    elif review_order == 2:
        retdata['order_info'] = '按总评排序：'
    elif review_order == 3:
        retdata['order_info'] = '按专业排序：'
    retdata['cur'] = review_page

    # print(retdata)
    return render(request, 'reviewlist.html', retdata)
    # except Exception as e:
    #     return HttpResponse(str(e))
