from datetime import datetime, timedelta
from time import sleep
from celery import shared_task
from django.utils.timezone import now
from .models import NextDayMeal, MealSchedule, Mess , Meal
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task(bind = True)
def test_func(self):
    # operation 

    for i in range(10):
        print(f'Hello - {i}')
    return 'Done'

@shared_task
def sleeptime(time):

    sleep(time)

    return None


@shared_task
def update_next_day_meal():
    current_time = now().time()  # Get current time (HH:MM)
    today = datetime.now() + timedelta(1)
    formating = datetime.strftime(today, "%A, %d-%b-%Y")
    messes = Mess.objects.all()  # Get all messes

    for mess in messes:
        if mess.meal_update_time.hour == current_time.hour and mess.meal_update_time.minute == current_time.minute:
            # Get users in this mess
            users = User.objects.filter(in_mess=mess)
            
            today_week = now().strftime("%a").lower() + timedelta(1)  # e.g., 'mon'
            
            for user in users:
                meal_today = MealSchedule.objects.filter(user=user, day=today_week).first()
                meal_yesterday = NextDayMeal.objects.filter(user=user).first()
                if meal_today:
                    # Update NextDayMeal
                    NextDayMeal.objects.update(
                        user=user,
                        mess=user.in_mess,
                        lunch= meal_today.lunch, 
                        dinner= meal_today.dinner, 
                        day= today
                    )

                    # create meal data for each user
                    Meal.objects.create(
                        user=user,
                        mess=user.in_mess,
                        lunch= meal_yesterday.lunch, 
                        dinner= meal_yesterday.dinner 
                    )
