from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from schools.models import School, Review
from django.core import serializers

import jieba

# 主页面
def index(request):
    return render(request, 'index.html')


# about界面
def about(request):
    return render(request, 'about.html')

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


# 学校详情页面
def school_detail(request, id):
    try:
        school = School.objects.get(id=id)
    except Exception as e:
        retdata = {
            'status': False,
            'info': str(e),
        }
        return render(request, 'school.html', {'school': None})

    if request.method == 'GET':
        # serializer = SchoolSerializer(school)
        # retdata = serializer.data
        # retdata['status'] = True
        return render(request, 'school.html', {'school': school})

# 评论页面


def newreview(request):
    return render(request, 'review.html')

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
