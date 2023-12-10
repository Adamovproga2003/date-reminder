import datetime

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import DateForm, monthDay
from .models import Person
from .utils import check_leap


def index(request):
    today = datetime.datetime.now().date()
    seven_days_later = today + datetime.timedelta(days=7)

    all_persons = Person.objects.all()

    latest_persons = []
    for person in all_persons:
        birthday_month_day = person.birthDay.strftime("%m-%d")

        # Create date objects for this year's birthday

        current_year = datetime.datetime.now().year

        this_years_birthday = None
        if person.birthDay.month == 2 and not check_leap(current_year):
            if person.birthDay.day == 29:
                this_years_birthday = datetime.datetime.strptime(f"{datetime.datetime.now().year}-{person.birthDay.month}-{person.birthDay.day - 1}",
                                                             "%Y-%m-%d").date()
        else:
            this_years_birthday = datetime.datetime.strptime(f"{datetime.datetime.now().year}-{birthday_month_day}",
                                                             "%Y-%m-%d").date()
        if this_years_birthday:
            if today <= this_years_birthday <= seven_days_later:
                latest_persons.append({
                    "id": person.id,
                    "name": person.name,
                    'relationship': person.relationship,
                    "difference": datetime.datetime.now().year - int(person.birthDay.strftime('%Y'))
                })

    current_date = datetime.datetime.now() + datetime.timedelta(days=7)
    context = {"latest_persons": latest_persons, "current_date": current_date}
    return render(request, "reminder/index.html", context)


def create(request):
    form = DateForm()
    return render(request, "reminder/add.form.html", {"form": form})


def edit(request, person_id):
    person = Person.objects.get(pk=person_id)
    date = datetime.datetime.strptime(str(person.birthDay), "%Y-%m-%d")
    day = date.day
    year = date.year
    month = list(monthDay.keys())[date.month - 1]
    name = person.name
    relationship = person.relationship
    form = DateForm({"day": day, "year": year, "month": month, "name": name, "relationship": relationship})
    return render(request, "reminder/change.form.html", {"form": form})


def delete(request, person_id):
    person = Person.objects.get(pk=person_id)
    person.delete()
    return HttpResponseRedirect(reverse("index"))


def add(request):
    if request.method == "POST":
        form = DateForm(request.POST)
        print("request.POST", request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            relationship = form.cleaned_data['relationship']
            month = list(monthDay.keys()).index(form.cleaned_data['month']) + 1
            day = form.cleaned_data['day']
            year = form.cleaned_data['year']
            date = datetime.datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d')
            person = Person(name=name, relationship=relationship, birthDay=date)
            person.save()
        else:
            return render(request, "reminder/add.form.html", {"form": form})
    return HttpResponseRedirect(reverse("index"))
