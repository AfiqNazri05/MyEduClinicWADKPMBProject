from django.shortcuts import render, redirect, get_object_or_404
from myeduclinic.models import Mentor, Student, Subject, Tuition
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.db import IntegrityError
import uuid
# Create your views here.
def login (request) : 
    return render (request, "login.html")

def signup(request):
    return render(request, 'signup.html')

def signupstudent(request):
    if request.method == "POST":
        studentid1 = request.POST["studentid"]
        studentname1 = request.POST["studentname"]
        studentcourse1 = request.POST["studentcourse"]
        studentphonenum1 = request.POST["studentphonenum"]
        studentemail1 = request.POST["studentemail"]
        studentpassword1 = request.POST["studentpassword"]

        
        new_student = Student(studentid=studentid1, studentname=studentname1, studentcourse = studentcourse1, studentphonenum = studentphonenum1, studentemail=studentemail1,studentpassword=studentpassword1)
        new_student.save()

        return HttpResponseRedirect(reverse("login"))
    
    return render(request, "signupstudent.html")
    
def signupmentor (request) : 
    if request.method == "POST" :
        mentorid1 = request.POST["mentorid"]
        mentorname1 = request.POST["mentorname"]
        mentoremail1 = request.POST["mentoremail"]
        mentorpassword1 = request.POST["mentorpassword"]

        datasignupmentor = Mentor(mentorid = mentorid1, mentorname = mentorname1, mentoremail = mentoremail1, mentorpassword = mentorpassword1)
        datasignupmentor.save()

        return HttpResponseRedirect(reverse("login"))
    
    return render(request, "signupmentor.html")
    
def signinstudent(request):
    if request.method == "POST":
        studentemail2 = request.POST["studentemail"]
        studentpassword2 = request.POST["studentpassword"]

        signupstudent = Student.objects.filter(studentemail=studentemail2, studentpassword=studentpassword2).first()

        if signupstudent:
            return redirect('studenthomepage', studentid=signupstudent.studentid)
        else:
            return render(request, 'signinstudent.html', {'error': 'Invalid Credentials'})
        
    return render(request, 'signinstudent.html')

def signinmentor(request):
    if request.method == "POST":
        mentoremail2 = request.POST.get("mentoremail")
        mentorpassword2 = request.POST.get("mentorpassword")

        # Authenticate mentor
        signupmentor = Mentor.objects.filter(mentoremail=mentoremail2, mentorpassword=mentorpassword2).first()

        if signupmentor:
            # Set mentor in session
            request.session['mentorid'] = signupmentor.mentorid
            return HttpResponseRedirect(reverse('mentorhomepage'))
        else:
            return render(request, 'signinmentor.html', {'error': 'Invalid Credentials'})

    return render(request, "signinmentor.html")


def studenthomepage(request, studentid=None):
    # If studentid is provided, use it; otherwise, fallback to session
    if studentid:
        try:
            mystudent = Student.objects.get(studentid=studentid)
        except Student.DoesNotExist:
            mystudent = None
    else:
        student_id = request.session.get('studentid')
        if student_id:
            try:
                mystudent = Student.objects.get(studentid=student_id)
            except Student.DoesNotExist:
                mystudent = None
        else:
            mystudentname = request.GET.get("studentname", None)
            if mystudentname:
                mystudent = Student.objects.filter(studentname=mystudentname).first()
            else:
                mystudent = None

    # Prepare the context for rendering the template
    context = {
        'mystudent': mystudent,
        'mytuition': [],
    }

    # If a student is found, retrieve their tuition records
    if mystudent:
        mytuition = Tuition.objects.filter(tuitionstudentid=mystudent).select_related('tuitionmentorid', 'subjectcode')
        context['mytuition'] = mytuition

    return render(request, "studenthomepage.html", context)


def mentorhomepage(request):
    mentorid = request.session.get('mentorid')

    if mentorid:
        mymentor = Mentor.objects.filter(mentorid=mentorid).first()
        
        if mymentor:
            # Filter tuition records to exclude those already assigned to a student
            mytuition = Tuition.objects.filter(tuitionmentorid=mymentor).exclude(tuitionstudentid__isnull=False).select_related('subjectcode')

            context = {
                'mymentor': mymentor,
                'mytuition': mytuition,
            }
        else:
            context = {
                'mymentor': None,
                'mytuition': [],
            }
    else:
        return HttpResponseRedirect(reverse('signinmentor'))

    return render(request, 'mentorhomepage.html', context)


def newtuition(request):
    mymentor = Mentor.objects.all().values()

    if request.method == "POST":
        # Get the form data
        tuitioncode1 = request.POST.get("tuitioncode")
        tuitionstudentid1 = request.POST.get("tuitionstudentid")
        tuitionmentorid1 = request.POST.get("tuitionmentorid")
        subjectcode1 = request.POST.get("subjectcode")
        tuitionmeet1 = request.POST.get("tuitionmeet")
        tuitiondate1 = request.POST.get("tuitiondate")
        tuitionduration1 = request.POST.get("tuitionduration")

        studentnew = Student.objects.filter(studentid=tuitionstudentid1).first()
        mentornew = Mentor.objects.filter(mentorid=tuitionmentorid1).first()
        subjectnew = Subject.objects.filter(subjectcode=subjectcode1).first()

        if studentnew is None or mentornew is None or subjectnew is None:
            message = "Invalid input: Student, Mentor, or Subject not found."
            return render(request, 'newtuition.html', {
                'mymentor': mymentor,
                'message': message,
            })

        datatuition = Tuition(
            tuitioncode=tuitioncode1,
            tuitionstudentid=studentnew,
            tuitionmentorid=mentornew,
            subjectcode=subjectnew,
            tuitionmeet=tuitionmeet1,
            tuitiondate=tuitiondate1,
            tuitionduration=tuitionduration1
        )
        datatuition.save()

        tuition1 = Tuition.objects.filter(tuitionstudentid=studentnew).select_related('tuitionmentorid', 'subjectcode')

        context = {
            'mystudent': studentnew,
            'mymentor': mymentor,
            'mysubject': Subject.objects.all(),
            'mytuition': tuition1, 
            'message': "NEW TUITION HAS BEEN SAVED"
        }
        return render(request, 'studenthomepage.html', context)

    else:
        mystudent = None
        tuition1 = Tuition.objects.filter(tuitionstudentid=mystudent).select_related('tuitionmentorid', 'subjectcode') if mystudent else []
        context = {
            'mystudent': mystudent,
            'mymentor': mymentor,
            'mysubject': Subject.objects.all(),
            'mytuition': tuition1
        }
        return render(request, 'newtuition.html', context)


def registertution(request):
    if request.method == "POST":
        mentorid1 = request.POST.get("mentorid")
        mentorname1 = request.POST.get("mentorname")
        mentorcourse1 = request.POST.get("mentorcourse")
        mentorphonenum1 = request.POST.get("mentorphonenum")
        subjectcode1 = request.POST.get("subjectcode")
        subjectname1 = request.POST.get("subjectname")
        mentormeet1 = request.POST.get("mentormeet")  

        new_mentor, created = Mentor.objects.get_or_create(
            mentorid=mentorid1,
            defaults={
                'mentorname': mentorname1,
                'mentorcourse': mentorcourse1,
                'mentorphonenum': mentorphonenum1,
                'mentormeet': mentormeet1
            }
        )

        if not created:
            new_mentor.mentorname = mentorname1
            new_mentor.mentorcourse = mentorcourse1
            new_mentor.mentorphonenum = mentorphonenum1
            new_mentor.mentormeet = mentormeet1
            new_mentor.save()

        new_subject, created = Subject.objects.get_or_create(
            subjectcode=subjectcode1,
            defaults={
                'subjectname': subjectname1,
                'mentorsubject': new_mentor,
                'mentormeet': mentormeet1 
            }
        )

        if not created:
            new_subject.subjectname = subjectname1
            new_subject.mentorsubject = new_mentor
            new_subject.mentormeet = mentormeet1
            new_subject.save()

        unique_tuitioncode = str(uuid.uuid4())[:5]
        Tuition.objects.create(
            tuitioncode=unique_tuitioncode,
            tuitionmentorid=new_mentor,
            subjectcode=new_subject
        )

        return HttpResponseRedirect(reverse("mentorhomepage"))

    return render(request, 'registertution.html')


def updatestudentprofile(request, studentid):
    try:
        student = Student.objects.get(studentid=studentid)
    except Student.DoesNotExist:
        return render(request, "error.html", {'message': 'Student not found'})

    if request.method == 'POST':
        student.studentname = request.POST.get('studentname', student.studentname)
        student.save()
        return redirect('studenthomepage', studentid=student.studentid)

    return render(request, "updatestudentprofile.html", {'student': student})


def updatestudentdata(request, studentid):
    data = Student.objects.get(studentid=studentid)
    studentname = request.POST.get('studentname')
    studentemail = request.POST.get('studentemail')
    studentpassword = request.POST.get('studentpassword')
    studentphonenum = request.POST.get('studentphonenum')

    if studentname and studentemail and studentpassword and studentphonenum:
        data.studentname = studentname
        data.studentemail = studentemail
        data.studentpassword = studentpassword
        data.studentphonenum = studentphonenum
        data.save()
        return redirect('studenthomepage', studentid=studentid)
    else:
        return render(request, "updatestudentprofile.html", {
            'updateid': data,
            'message': 'All fields are required!'
        })

def updatetuition(request, studentid, tuitioncode):
    try:
        tuition = Tuition.objects.get(tuitioncode=tuitioncode, tuitionstudentid=studentid)
    except Tuition.DoesNotExist:
        return render(request, "error.html", {'message': 'Tuition not found'})

    if request.method == 'POST':
        tuition.tuitionmeet = request.POST.get('tuitionmeet', tuition.tuitionmeet)
        tuition.tuitiondate = request.POST.get('tuitiondate', tuition.tuitiondate)
        tuition.tuitionduration = request.POST.get('tuitionduration', tuition.tuitionduration)
        tuition.save()
        return redirect('studenthomepage', studentid=tuition.tuitionstudentid.studentid)

    return render(request, "updatetuition.html", {'updateid': tuition})

def updatetuitiondata(request, tuitioncode):
    try:
        data = Tuition.objects.get(tuitioncode=tuitioncode)
        tuitionmeet = request.POST.get('tuitionmeet')
        tuitiondate = request.POST.get('tuitiondate')
        tuitionduration = request.POST.get('tuitionduration')

        if tuitionmeet and tuitiondate and tuitionduration:
            data.tuitionmeet = tuitionmeet
            data.tuitiondate = tuitiondate
            data.tuitionduration = tuitionduration
            data.save()

            return redirect('studenthomepage', studentid=data.tuitionstudentid.studentid)
        else:
            return render(request, "updatetuition.html", {
                'updateid': data,
                'message': 'All fields are required!'
            })
    except Tuition.DoesNotExist:
        return render(request, "error.html", {'message': 'Tuition not found'})

def updatementor(request, mentorid):
    updateid = Mentor.objects.get(mentorid=mentorid)
    mymentor = Mentor.objects.all()
    
    context = {
        'updateid': updateid,
        'mymentor': mymentor,
        'message': 'PAGE RENDERED, DATA IS NOT UPDATED YET'
    }
    return render(request, "updatementor.html", context)

def updatementordata(request, mentorid):
    updateid = get_object_or_404(Mentor, mentorid=mentorid)

    if request.method == "POST":
        mentorname = request.POST.get('mentorname')
        mentorcourse = request.POST.get('mentorcourse')
        mentorphonenum = request.POST.get('mentorphonenum')
        subjectcode = request.POST.get('subjectcode')
        subjectname = request.POST.get('subjectname')
        mentormeet = request.POST.get('mentormeet')

        updateid.mentorname = mentorname
        updateid.mentorcourse = mentorcourse
        updateid.mentorphonenum = mentorphonenum
        updateid.save()

        try:
            subject = Subject.objects.get(subjectcode=subjectcode)
            subject.subjectname = subjectname
            subject.mentorsubject = updateid
            subject.mentormeet = mentormeet 
            subject.save()
        except Subject.DoesNotExist:
            new_subject = Subject.objects.create(
                subjectcode=subjectcode,
                subjectname=subjectname,
                mentorsubject=updateid,
                mentormeet=mentormeet 
            )
            Tuition.objects.create(
                tuitionmentorid=updateid,
                subjectcode=new_subject
            )

        return redirect('mentorhomepage')

    subject = Subject.objects.filter(mentorsubject=updateid).first()
    context = {
        'updateid': updateid,
        'subjectcode': subject.subjectcode,
        'subjectname': subject.subjectname,
        'mentormeet': subject.mentormeet
    }

    return render(request, 'updatementor.html', context)

def deletetuition(request, tuitioncode):
    try:
        datanakdelete = Tuition.objects.get(tuitioncode=tuitioncode)
    except Tuition.DoesNotExist:
        return HttpResponse("Tuition not found", status=404)

    return render(request, "deletetuition.html", {'datatobedeleted': datanakdelete})

def deletetuitiondata(request, tuitioncode):
    deletementor = Tuition.objects.get(tuitioncode=tuitioncode)
    studentid = deletementor.tuitionstudentid.studentid
    deletementor.delete()
    return HttpResponseRedirect(reverse("studenthomepage", args=[studentid]))

def deletementor(request, subjectcode):
    subject_to_delete = get_object_or_404(Subject, subjectcode=subjectcode)
    
    if request.method == 'POST':
        subject_to_delete.delete()
        return redirect('mentorhomepage')
    
    return render(request, "deletementordata.html", {'datatobedeleted': subject_to_delete})

def deletementordata(request, subjectcode):
    if request.method == 'POST':
        subject_to_delete = get_object_or_404(Subject, subjectcode=subjectcode)

        Tuition.objects.filter(subjectcode=subject_to_delete).delete()
        subject_to_delete.delete()

        return HttpResponseRedirect(reverse("mentorhomepage"))
    return HttpResponse("Invalid request method.", status=405)

def searchtuition(request):
    query = request.GET.get('search')
    student_id = request.session.get('studentid')
    
    student = None
    if student_id:
        try:
            student = Student.objects.get(studentid=student_id)
        except Student.DoesNotExist:
            student = None  # student will remain None

    findtuition = Tuition.objects.filter(
        Q(tuitioncode__icontains=query) |
        Q(tuitionmentorid__mentorid__icontains=query) |
        Q(tuitiondate__icontains=query) |
        Q(subjectcode__subjectcode__icontains=query)
    ) if query else Tuition.objects.none()

    context = {
        'mytuition': findtuition,
        'student': student,
    }
    return render(request, 'searchtuition.html', context)
