from holidaylist.models import HolidayList
from datetime import datetime, timedelta, date
from notices.models import Notice
from main_app.models import UserProfile
from django.utils import timezone


def run():
    holiday = HolidayList.objects.filter(date= date.today() + timedelta(days=1) )
    for h in holiday:
        all_users = UserProfile.objects.filter(institute=h.institute)
        holiday_notice = Notice.objects.create(institute = h.institute, category ="Holiday", subject =f"Holiday declared on {h.date}", content=f"School will remain closed on {h.date} on account of {h.name} ", created_at= timezone.now(), publish_date= timezone.now() )

        for u in all_users: # adding all users of that institute to the recepient list of notice
            holiday_notice.recipients_list.add(u)
        