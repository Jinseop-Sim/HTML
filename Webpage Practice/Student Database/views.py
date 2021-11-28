from django.shortcuts import render, redirect
from .models import Students

def display(request):
    students = Students.objects.all().order_by('id')
    return render(request, 'myApp/index.html', {"students" : students})

def edit_record(request,student_id):
    if request.method == 'POST':
        id = request.POST['id']
        firstname = request.POST['fn']
        secondname = request.POST['sn']
        age = request.POST['age']
        major = request.POST['major']
        address = request.POST['addr']

        stu = Students.objects.get(id = id)
        stu.id = id
        stu.firstname = firstname
        stu.secondname = secondname
        stu.age = age
        stu.major = major
        stu.address = address
        stu.save()
        return redirect('index')
    else:
        student = Students.objects.get(id = student_id)
        return render(request, 'myApp/edit.html',{"student":student})

def add_record(request):
    if request.method == 'POST':
        student = Students()
        student.id = request.POST['id']
        student.firstname = request.POST['fn']
        student.secondname = request.POST['sn']
        student.age = request.POST['age']
        student.major = request.POST['major']
        student.address = request.POST['addr']
        student.save()
        return redirect('index')
    else:
        return render(request, 'myApp/addrecord.html')

def delete_record(request, student_id):
    if request.method == "POST":
        student = Students.objects.get(id = student_id)
        student.delete()
        return redirect('index')
    else:
        return render(request, 'index')
