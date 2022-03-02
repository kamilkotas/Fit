from django.shortcuts import render, redirect
from .forms import DesirableIntakeForm, AddFoodForm
from .models import Profile, FoodItem, History
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView, UpdateView


def home(request):
    if request.method == "GET":
        form = DesirableIntakeForm()
        add_form = AddFoodForm()
        print(request.user)
        if request.user.is_authenticated:
            app_user = Profile.objects.get(user_id=request.user)
            calories = 0
            protein = 0
            carbs = 0
            fats = 0

            for food in app_user.foods.all():
                calories += food.calories * food.quantity
                protein += food.protein * food.quantity
                carbs += food.carbs * food.quantity
                fats += food.fats * food.quantity

            cal_left = app_user.desirable_intake - calories
            context = {"form": form, "app_user": app_user, 'calories': calories,
                        'protein': protein, "carbs": carbs, "fats": fats, 'cal_left': cal_left,
                       'add_form': add_form}
            return render(request, "index.html", context)
        else:
            return render(request, "index.html",)
    if request.method == "POST":
        form = DesirableIntakeForm(request.POST)
        add_form = AddFoodForm(request.POST)
        profile = Profile.objects.get(user_id=request.user)
        current_user = request.user
        if add_form.is_valid():
            for food in add_form.cleaned_data["foods"]:
                profile.foods.add(food.id)
        if form.is_valid():
            user = User.objects.get(id=current_user.id)
            Profile.objects.update_or_create(
                user=user,
                defaults={"desirable_intake": form.cleaned_data["desirable_intake"]}
            )
        return redirect("/")


class AddFoodView(CreateView):
    model = FoodItem
    fields = "__all__"
    success_url = "/"


class FoodItemList(ListView):
    model = FoodItem


class UpdateFoodView(UpdateView):
    model = FoodItem
    fields = "__all__"
    success_url = "/"


def delete(request, pk, id):
    profile = Profile.objects.get(id=pk)
    food = FoodItem.objects.get(id=id)
    if request.method == "POST":
        profile.foods.remove(food)
        return redirect("/")
    else:
        context = {"food": food}
        return render(request, "Calculator/delete_food.html", context)


def add_history(request):
    if request.method == "GET":
        return render(request, "Calculator/add_history.html")

    if request.method == "POST":
            app_user = Profile.objects.get(user_id=request.user)
            calories = 0
            protein = 0
            carbs = 0
            fats = 0

            for food in app_user.foods.all():
                calories += food.calories
                protein += food.protein
                carbs += food.carbs
                fats += food.fats
            History.objects.create(
                day_calories=calories,
                day_protein=protein,
                day_carbs=carbs,
                day_fats=fats,
            )
            return redirect("/")


def history(request):
    if request.method == "GET":
        history = History.objects.all
        context = {"history": history}
        return render(request, "Calculator/history.html", context)


def del_all_foods(request):
    if request.method == "GET":
        return render(request, "Calculator/del_all.html")
    if request.method == "POST":
        profile = Profile.objects.get(id=request.user.id)
        for food in profile.foods.all():
            profile.foods.remove(food)
        return redirect("/")
