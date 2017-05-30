import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zhaoxiao.settings")

import django
import csv


def main():
    first = True
    univ = []
    with open('universityInfo.CSV', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            # print(row)
            if first:
                first = False
                continue
            else:
                univ.append(row[1:])
    # print(univ)
    from schools.models import School
    for un in univ:
        School.objects.create(name=un[0], administration_dept=un[1], location=un[2], level=un[3])
    # f = open('oldblog.txt')
    # for line in f:
    #     title,content = line.split('****')
    #     Blog.objects.create(title=title,content=content)
    # f.close()

if __name__ == "__main__":
    django.setup()
    main()
    print('Done!')
