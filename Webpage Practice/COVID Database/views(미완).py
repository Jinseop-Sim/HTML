from django.db import connection
from django.shortcuts import render, redirect
import pandas as pd

def initial_page(request):
    with connection.cursor() as cursor:
        initQuery1 = "DELETE FROM students"
        cursor.execute(initQuery1)
        initQuery2 = "DELETE FROM professors"
        cursor.execute(initQuery2)
        initQuery3 = "DELETE FROM counties"
        cursor.execute(initQuery3)
        initQuery4 = "DELETE FROM covid"
        cursor.execute(initQuery4)

    return render(request, 'myApp/index.html')

def display(request):
    StudOutput = []
    ProfOutput = []
    countiesOutput = []
    covidOutput = []
    Q1 = []
    Q2 = []
    Q3 = []
    Q4 = []
    Q5 = []

    with connection.cursor() as cursor:
        studQuery = "SELECT * FROM students"
        cursor.execute(studQuery)
        fetchResultStud = cursor.fetchall()

        profQuery = "SELECT * FROM professors"
        cursor.execute(profQuery)
        fetchResultProf = cursor.fetchall()

        countQuery = "SELECT * FROM counties"
        cursor.execute(countQuery)
        fetchResultCount = cursor.fetchall()

        covidQuery = "SELECT * FROM covid ORDER BY covid.patientID*1"
        cursor.execute(covidQuery)
        fetchResultCovid = cursor.fetchall()

        Query1 = "SELECT students.county, ROUND(AVG(students.score), 2) " \
                 "FROM students " \
                 "GROUP BY students.county "
        cursor.execute(Query1)
        fetchResultQ1 = cursor.fetchall()

        Query2 = "SELECT counties.city AS city, ROUND(AVG(score), 2) AS averageScore " \
                 "FROM counties, students " \
                 "WHERE students.county = counties.countyName " \
                 "GROUP BY counties.city "
        cursor.execute(Query2)
        fetchResultQ2 = cursor.fetchall()

        Query3 = "SELECT Profinfo.name, Studinfo.name " \
                 "FROM (SELECT professors.name, Agetable.county" \
                 "      FROM (SELECT professors.county, MAX(professors.age) AS elder_age" \
                 "            FROM professors" \
                 "            GROUP BY professors.county) Agetable, professors" \
                 "      WHERE professors.age = Agetable.elder_age AND professors.county = Agetable.county) Profinfo, " \
                 "      (SELECT students.name, Scoretable.county" \
                 "       FROM (SELECT students.county, MAX(students.score) AS highest_score" \
                 "             FROM students" \
                 "             GROUP BY students.county) Scoretable, students" \
                 "       WHERE students.score = Scoretable.highest_score AND students.county = Scoretable.county) Studinfo " \
                 "WHERE Profinfo.county = Studinfo.county "
        cursor.execute(Query3)
        fetchResultQ3 = cursor.fetchall()

        Query4 = "SELECT Profinfo.name, Studinfo.name " \
                 "FROM (SELECT professors.name, Agetable.city " \
                 "      FROM (SELECT counties.city, newTable.elder_age, counties.countyName " \
                 "            FROM (SELECT counties.city, MAX(professors.age) AS elder_age " \
                 "	                FROM professors JOIN counties " \
                 "	                ON professors.county = counties.countyName " \
                 "		            GROUP BY counties.city) newTable JOIN counties " \
                 "	          ON counties.city = newTable.city) Agetable, professors " \
                 "      WHERE professors.age = Agetable.elder_age AND professors.county = Agetable.countyName) Profinfo, " \
                 "     (SELECT students.name, Scoretable.city" \
                 "      FROM (SELECT counties.city, newStudTable.highest_score, counties.countyName " \
                 "	          FROM (SELECT counties.city, MAX(students.score) AS highest_score " \
                 "		            FROM students JOIN counties " \
                 "		            ON students.county = counties.countyName " \
                 "                  GROUP BY counties.city) newStudTable JOIN counties " \
                 "            ON counties.city = newStudTable.city) Scoretable, students " \
                 "      WHERE students.score = Scoretable.highest_score AND students.county = Scoretable.countyName) Studinfo " \
                 "WHERE Profinfo.city = Studinfo.city "
        cursor.execute(Query4)
        fetchResultQ4 = cursor.fetchall()

        Query5 = "SELECT students.name, TOP_three.city " \
                 "FROM (SELECT patient_table.city, patient_table.patient_number / SUM(counties.population) AS ratio " \
                 "      FROM (SELECT covid.city, COUNT(covid.city) as patient_number " \
                 "            FROM covid " \
                 "            GROUP BY covid.city) patient_table, counties " \
                 "      WHERE counties.city = patient_table.city " \
                 "      GROUP by counties.city " \
                 "      ORDER BY ratio DESC " \
                 "      LIMIT 3) TOP_three, students, counties " \
                 "WHERE counties.city = TOP_three.city AND students.county = counties.countyName "
        cursor.execute(Query5)
        fetchResultQ5 = cursor.fetchall()

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

        for temp in fetchResultQ1:
            eachRow = {'countyName':temp[0], 'averageScore':temp[1]}
            Q1.append(eachRow)

        for temp in fetchResultQ2:
            eachRow = {'city':temp[0], 'averageScore':temp[1]}
            Q2.append(eachRow)

        for temp in fetchResultQ3:
            eachRow = {'profname':temp[0], 'studname':temp[1]}
            Q3.append(eachRow)

        for temp in fetchResultQ4:
            eachRow = {'profname':temp[0], 'studname':temp[1]}
            Q4.append(eachRow)

        for temp in fetchResultQ5:
            eachRow = {'studname':temp[0], 'city':temp[1]}
            Q5.append(eachRow)

    return render(request, 'myApp/index.html', {'students':StudOutput, 'professors':ProfOutput,
                                                'counties':countiesOutput, 'covid':covidOutput, 'Q1':Q1, 'Q2':Q2, 'Q3':Q3, 'Q4':Q4, 'Q5':Q5})

def insert_stud(request):
    stud_csv = pd.read_csv("./myApp/templates/myApp/students.csv", header=None)
    stud_csv.columns = ['studentID', 'name', 'score', 'county']

    for i in range(len(stud_csv)):
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

def insert_prof(request):
    prof_csv = pd.read_csv("./myApp/templates/myApp/professors.csv", header=None)
    prof_csv.columns = ['facultyID', 'name', 'age', 'county']

    for i in range(len(prof_csv)):
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

def insert_counties(request):
    count_csv = pd.read_csv("./myApp/templates/myApp/counties.csv", header=None)
    count_csv.columns = ['countyName', 'population', 'city']

    for i in range(len(count_csv)):
        cntName = count_csv.iloc[i]['countyName']
        popul = int(count_csv.iloc[i]['population'])
        city = count_csv.iloc[i]['city']

        with connection.cursor() as cursor:
            inQuery = "INSERT INTO counties (countyName, population, city) VALUES('{}', '{}', '{}')"
            cursor.execute(inQuery.format(cntName, popul, city))

            connection.commit()
            connection.close()

    return redirect('index')

def insert_covid(request):
    covidOutput = []
    covid_csv = pd.read_csv("./myApp/templates/myApp/covid.csv", header=None)
    covid_csv.columns = ['patientID', 'city']

    for i in range(len(covid_csv)):
        patID = covid_csv.iloc[i]['patientID']
        city = covid_csv.iloc[i]['city']

        with connection.cursor() as cursor:
            inQuery = "INSERT INTO covid (patientID, city) VALUES('{}', '{}')"
            cursor.execute(inQuery.format(patID, city))

            connection.commit()
            connection.close()

    return redirect('index')
