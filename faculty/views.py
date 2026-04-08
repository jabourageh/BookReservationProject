from django.shortcuts import render
from django.http import HttpResponse
from faculty.models import StudentDetails, BookDetails, BookReservation
from django.db import connection 
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required 
from django.db.models import Avg, Count, Min, Max

# Create your views here.
@login_required 

def home(request):
    # django will look for the factulty directory inside templates and look for home.http
    return render(request, 'faculty/home.html')
    #return HttpResponse("This is the home page")

def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# usuing django template langauge : 
#1) allows integrating data into the HTML
#2) Allows us to add python like utilities (if conditon, for loops) in the HTML 
@login_required 
def student_details(request):
    #context = {"name": "Steve Sides"}
    #django query set is djangos's abrstraction of  SQL. If a table was created via django we can use the django Query set
    data = StudentDetails.objects.all()
    # The above statemnt is equal to the SQL Statement : SELECT * FROM facultydetails;
    #data = dictfetchall(cursor)

    #cursor = connection.cursor()
    #cursor.execute("select * from faculty_studentdetails")
    data = StudentDetails.objects.all()
    paginator = Paginator(data,10)
    page = request.GET.get("page")
    page_data= paginator.get_page(page)
    context = {"studentdetails": page_data}
    return render(request, 'faculty/studentdetails.html', context)
@login_required 
def book_details(request):
    #django query set is djangos's abrstraction of  SQL. If a table was created via django we can use the django Query set
    data = BookDetails.objects.all()
    # The above statemnt is equal to the SQL Statement : SELECT * FROM facultydetails;
    #data = dictfetchall(cursor)

    #cursor = connection.cursor()
    #cursor.execute("select * from faculty_facultydetails")
    data = BookDetails.objects.all().order_by('-numberoftimescheckedout') 
    paginator = Paginator(data,10)
    page = request.GET.get("page")
    page_data= paginator.get_page(page)
    context = {"bookdetails": page_data}
    return render(request, 'faculty/bookdetails.html', context)


@login_required 
def book_reservation(request):
    student_data = StudentDetails.objects.all()
    book_data = BookDetails.objects.filter(currentlycheckedout=False)
    reservation_data = BookReservation.objects.select_related('studentid', 'bookid').all().order_by('-id')

    context = {"student":student_data,"book":book_data, "bookreservation": reservation_data}

    return render(request,"faculty/bookreservation.html",context)

def savereservation(request):
    #print(request.__dict__)
    if "studentid" in request.GET and "bookid" in request.GET:

        studentid = request.GET.get("studentid")
        bookid = request.GET.get("bookid")

        print("STUDENT:", studentid)
        print("BOOK:", bookid)

        if not studentid or not bookid:
            return HttpResponse("error")
    


        studentobject = StudentDetails.objects.filter(studentid=studentid).first()
        bookobject = BookDetails.objects.filter(bookid=bookid).first()

        if not studentobject or not bookobject:
            return HttpResponse("error")

        # RULE 1: Same student cannot reserve same book twice
        if BookReservation.objects.filter(studentid=studentid, bookid=bookid).exists():
            return HttpResponse("already_exists")

        # RULE 2: Student cannot reserve more than 4 books
        if BookReservation.objects.filter(studentid=studentid).count() >= 4:
            return HttpResponse("limit_reached")

        # RULE 3: No two students can reserve the same book
        if BookReservation.objects.filter(bookid=bookid).exists():
            return HttpResponse("book_unavailable")

        # CREATE RESERVATION
        BookReservation.objects.create(
            studentid=studentobject,
            bookid=bookobject
        )

        # RULE 4: UPDATE BOOK DETAILS TABLE
        bookobject.currentlycheckedout = True
        bookobject.numberoftimescheckedout += 1
        bookobject.save()
        print("SAVED TO DATABASE")




        return HttpResponse("success")

    return HttpResponse("error")

@login_required
def dashboard(request):
    # Total number of students
    studentcount = StudentDetails.objects.count()

    # Average GPA
    avg_gpa = StudentDetails.objects.aggregate(Avg('gpa'))['gpa__avg'] or 0

    # Number of students by year
    seniors = StudentDetails.objects.filter(year="Senior").count()
    juniors = StudentDetails.objects.filter(year="Junior").count()
    sophomores = StudentDetails.objects.filter(year="Sophomore").count()
    freshmen = StudentDetails.objects.filter(year="Freshman").count()

    # Pass data to template
    context = {
        "studentcount": studentcount,
        "avg_gpa": round(avg_gpa, 2),
        "seniors": seniors,
        "juniors": juniors,
        "sophomores": sophomores,
        "freshmen": freshmen,
    }

    return render(request, "faculty/dashboard.html", context)