from django.shortcuts import render
from count.models import result
from django.core.mail import send_mail
import sqlite3


# Create your views here.
from django.http import HttpResponse


def index(request):
    try:
        conn=sqlite3.connect('file:DB.db?mode=rw', uri = True)
    except sqlite3.OperationalError:
        print("hi")
        return render(request,'index1.html')
    c = conn.cursor()
    res = c.execute("SELECT * from TREES;")
    ar = []
    for i in res.fetchall():
        br = []
        for j in i:
            # j=(float)(j)
            # print(j)
            br.append(j)
        ar.append(br)
    # print(type(ar[0]))

    # print(res.fetchall())
    # print(res.fetchall())
    context = {
        'results':ar
        # 'results':result.objects.all()
    }
    
    
    send_mail(
    'Vegetation management infoasys',
    'This message is from Hackwithinfy Team2. Alert: Please go on your website for more detail that how many trees should be cut immediately',
    'sunilmaurya1506@gmail.com',
    ['sunilmaurya1506@gmail.com','akhilreddymaram@outlook.com'],
    fail_silently=False,
    )
    


    return render(request,'index.html',context)

