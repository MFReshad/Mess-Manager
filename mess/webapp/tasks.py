from datetime import datetime, timedelta
from time import sleep
from celery import shared_task
from django.utils.timezone import now
from . models import NextDayMeal, MealSchedule, Mess , Meal
from django.contrib.auth import get_user_model

import logging

logger = logging.getLogger(__name__)

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
    # print("🔥🔥 Running update_next_day_meal task")
    # logger.debug("🟢 DEBUG: update_next_day_meal task started")
    # logger.info("🔵 INFO: update_next_day_meal task started")
    # logger.warning("🟠 WARNING: update_next_day_meal task started")
    # logger.error("🔴 ERROR: update_next_day_meal task started")
    current_time = datetime.now().time()  # Get current time (HH:MM)
    # print(f'🟠🔴 {current_time}')
    tomorrow = datetime.now() + timedelta(days=1)
    # print(f'🟠🟠🟠 {tomorrow}')
    today_week = tomorrow.strftime("%a").lower()
    # print(f'🔵🔵🔵 {today_week}')
    formating = datetime.strftime(tomorrow, "%A, %d-%b-%Y")
    messes = Mess.objects.all()  # Get all messes
    # print(f'🟢🔵 this is - {messes}')
    for mess in messes:
        if mess.meal_update_time.hour == current_time.hour and mess.meal_update_time.minute == current_time.minute:
            # Get users in this mess
            # print(f'🟢🔵 🟢🔵 ')
            users = User.objects.filter(in_mess=mess)
            # print(f'🟠🟠 {tomorrow}')
            today_week = tomorrow.strftime("%a").lower()  # e.g., 'mon'
            
            for user in users:
                # print(f'🟢🔵 🟢🔵 {user.username}')
                meal_today = MealSchedule.objects.filter(user=user, day=today_week).first()
                meal_yesterday = NextDayMeal.objects.filter(user=user).first()
                if meal_today:
                    # Update NextDayMeal
                    NextDayMeal.objects.update_or_create(
                        user=user,
                        defaults={  
                            'lunch': meal_today.lunch,
                            'dinner': meal_today.dinner,
                            'day': tomorrow
                        }
                    )
                    if meal_yesterday:
                        # create meal data for each user
                        Meal.objects.create(
                            user=user,
                            mess=user.in_mess,
                            lunch= meal_yesterday.lunch, 
                            dinner= meal_yesterday.dinner 
                        )
