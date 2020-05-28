# from holidaylist.models import HolidayList
# from datetime import datetime, timedelta, date
# from notices.models import Notification_Category
# from main_app.models import UserProfile

# def run():
#     holiday = HolidayList.objects.filter(date= date.today() + timedelta(days=1) )
#     for s in holiday:
#         all_users = UserProfile.objects.filter(institute=s.institute)
#         print(all_users)