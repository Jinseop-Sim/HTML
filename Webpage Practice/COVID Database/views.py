from django.db import connection
from django.shortcuts import render, redirect
import pandas as pd

def display(request):
    StudOutput = []
    ProfOutput = []
    countiesOutput = []
    covidOutput = []

    with connection.cursor() as cursor:
        initQuery1 = "DELETE FROM students"
        cursor.execute(initQuery1)
        initQuery2 = "DELETE FROM professors"
        cursor.execute(initQuery2)
        initQuery3 = "DELETE FROM counties"
        cursor.execute(initQuery3)
        initQuery4 = "DELETE FROM covid"
        cursor.execute(initQuery4)

        studQuery = "SELECT * FROM students"
        cursor.execute(studQuery)
        fetchResultStud = cursor.fetchall()

        profQuery = "SELECT * FROM professors"
        cursor.execute(profQuery)
        fetchResultProf = cursor.fetchall()

        countQuery = "SELECT * FROM counties"
        cursor.execute(countQuery)
        fetchResultCount = cursor.fetchall()

        covidQuery = "SELECT * FROM covid"
        cursor.execute(covidQuery)
        fetchResultCovid = cursor.fetchall()

        connection.commit()
        connection.close()

        for temp in fetchResultStud:
            eachRow = {'studentID': temp[0], 'name': temp[1], 'score': temp[2], 'county': temp[3]}
            StudOutput.append(eachRow)

        for temp in fetchResultProf:
            eachRow = {'facultyID': temp[0], 'name': temp[1], 'age': temp[2], 'county': temp[3]}
            ProfOutput.append(eachRow)

        for temp in fetchResultCount:
            eachRow = {'countyName': temp[0], 'population': temp[1], 'city': temp[2]}
            countiesOutput.append(eachRow)

        for temp in fetchResultCovid:
            eachRow = {'patientID': temp[0], 'city': temp[1]}
            covidOutput.append(eachRow)

    return render(request, 'myApp/index.html', {'students':StudOutput, 'professors':ProfOutput, 'counties':countiesOutput, 'covid':covidOutput})

def display_stud(request):
    stud_csv = pd.read_csv("./myApp/templates/myApp/Students.csv")
    stud_csv.columns = ['studentID', 'name', 'score', 'county']

    for i in range(0, len(stud_csv)):
        studID = stud_csv.iloc[i]['studentID']
        name = stud_csv.iloc[i]['name']
        score = float(stud_csv.iloc[i]['score'])
        county = stud_csv.iloc[i]['county']

        with connection.cursor() as cursor:
            inQuery = "INSERT INTO students (studentID, name, score, county) VALUES('{}', '{}', '{}', '{}')"
            cursor.execute(inQuery.format(studID, name, score, county))

            connection.commit()
            connection.close()

    return redirect('index')

def display_prof(request):
    prof_csv = pd.read_csv("./myApp/templates/myApp/professors.csv")
    prof_csv.columns = ['facultyID', 'name', 'age', 'county']

    for i in range(0, len(prof_csv)):
        facID = prof_csv.iloc[i]['facultyID']
        name = prof_csv.iloc[i]['name']
        age = int(prof_csv.iloc[i]['age'])
        county = prof_csv.iloc[i]['county']

        with connection.cursor() as cursor:
            inQuery = "INSERT INTO professors (facultyID, name, age, county) VALUES('{}', '{}', '{}', '{}')"
            cursor.execute(inQuery.format(facID, name, age, county))

            connection.commit()
            connection.close()

    return redirect('index')

def display_counties(request):
    count_csv = pd.read_csv("./myApp/templates/myApp/counties.csv")
    count_csv.columns = ['countyName', 'population', 'city']

    for i in range(0, len(count_csv)):
        cntName = count_csv.iloc[i]['countyName']
        popul = int(count_csv.iloc[i]['population'])
        city = count_csv.iloc[i]['city']

        with connection.cursor() as cursor:
            inQuery = "INSERT INTO counties (countyName, population, city) VALUES('{}', '{}', '{}')"
            cursor.execute(inQuery.format(cntName, popul, city))

            connection.commit()
            connection.close()

    return redirect('index')

def display_covid(request):
    covidOutput = []
    covid_csv = pd.read_csv("./myApp/templates/myApp/COVID.csv")
    covid_csv.columns = ['patientID', 'city']

    for i in range(0, len(covid_csv)):
        patID = covid_csv.iloc[i]['patientID']
        city = covid_csv.iloc[i]['city']

        with connection.cursor() as cursor:
            inQuery = "INSERT INTO covid (patientID, city) VALUES('{}', '{}')"
            cursor.execute(inQuery.format(patID, city))

            connection.commit()
            connection.close()

    return redirect('index')
