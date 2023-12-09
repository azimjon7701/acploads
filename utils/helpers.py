import datetime
import random

import requests
from django.db.models import Q
from django.utils import timezone

api_key = 'AIzaSyD7Sbuc2E76Ht-VIQefQFUgtD253lVRkXk'


def get_time_limit_hour_query():
    time_limit_hour = timezone.now() - timezone.timedelta(hours=24)
    return Q(published_date__gte=time_limit_hour)


def distance_by_places(source, dest):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

    try:
        r = requests.get(url + 'origins=' + source +
                         '&destinations=' + dest +
                         '&key=' + api_key)
        x = r.json()
        return x['rows'][0]['elements'][0]['distance']['value']
    except Exception as e:
        return None


# print(distance_by_places("New Jersey, США", "New Jersey, США"))

def get_data_or_none(data):
    return data if data != "" else None


def get_date_or_none(data):
    return datetime.datetime.strptime(data, "%Y-%m-%d") if data != "" else None


def generate_rand_username():
    return f'anycap{random.randint(1000000, 10000000)}'


def get_as_tg_username(username):
    return username if username.startswith('@') else '@' + username


def get_radius_str(data):
    return round(float(data)) if type(data) == 'float' else '-'


def get_data_str(data):
    return "-" if (data == None or data == "") else data


def get_data_price(data):
    if (data == None or data == ""):
        return '-'
    else:
        price_str = "{:0,.2f}".format(float(data))
        return "$ " + str(price_str)

def get_data_float(data):
    if (data == None or data == ""):
        return '-'
    else:
        price_str = "{:0,.1f}".format(float(data))
        return str(price_str)


def render_contact_by_type(type: str, data: str):
    if type == 'telegram':
        contact_link = data[1:] if data.startswith('@') else data
        contact = data if data.startswith('@') else '@' + data
        return f"""<i class=" c-theme-font" style="color: #4b4545 !important;"><svg style="top: 3px; position: relative;"  xmlns="http://www.w3.org/2000/svg" width="22" height="16" fill="currentColor" class="bi bi-telegram" viewBox="0 0 16 16">
                                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.287 5.906c-.778.324-2.334.994-4.666 2.01-.378.15-.577.298-.595.442-.03.243.275.339.69.47l.175.055c.408.133.958.288 1.243.294.26.006.549-.1.868-.32 2.179-1.471 3.304-2.214 3.374-2.23.05-.012.12-.026.166.016.047.041.042.12.037.141-.03.129-1.227 1.241-1.846 1.817-.193.18-.33.307-.358.336a8.154 8.154 0 0 1-.188.186c-.38.366-.664.64.015 1.088.327.216.589.393.85.571.284.194.568.387.936.629.093.06.183.125.27.187.331.236.63.448.997.414.214-.02.435-.22.547-.82.265-1.417.786-4.486.906-5.751a1.426 1.426 0 0 0-.013-.315.337.337 0 0 0-.114-.217.526.526 0 0 0-.31-.093c-.3.005-.763.166-2.984 1.09z"></path>
                            </svg></i><a style="padding-top: 3px !important;" class="contact-link" target="_blank" href = "https://t.me/{contact_link}"> {contact} </a>"""
    elif type == 'phone':
        return f"""<i class="c-theme-font" style="color: #4b4545 !important;">
                            <svg style="top: 3px; position: relative;"  xmlns="http://www.w3.org/2000/svg" width="22" height="16" fill="currentColor" class="bi bi-telephone-fill" viewBox="0 0 16 16">
                                <path fill-rule="evenodd" d="M1.885.511a1.745 1.745 0 0 1 2.61.163L6.29 2.98c.329.423.445.974.315 1.494l-.547 2.19a.678.678 0 0 0 .178.643l2.457 2.457a.678.678 0 0 0 .644.178l2.189-.547a1.745 1.745 0 0 1 1.494.315l2.306 1.794c.829.645.905 1.87.163 2.611l-1.034 1.034c-.74.74-1.846 1.065-2.877.702a18.634 18.634 0 0 1-7.01-4.42 18.634 18.634 0 0 1-4.42-7.009c-.362-1.03-.037-2.137.703-2.877L1.885.511z"></path>
                            </svg>
                        </i>&ensp; <a style="padding-top: 3px !important;"  class="contact-link" target="_blank"  href="tel:{data}">{data}</a>
                        """
    elif type == 'email':
        return f"""<i class="c-theme-font" style="color: #4b4545 !important;">
                            <svg style="top: 3px; position: relative;" xmlns="http://www.w3.org/2000/svg" width="22" height="16" fill="currentColor" class="bi bi-envelope-fill" viewBox="0 0 16 16">
                                <path d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414.05 3.555ZM0 4.697v7.104l5.803-3.558L0 4.697ZM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586l-1.239-.757Zm3.436-.586L16 11.801V4.697l-5.803 3.546Z"></path>
                            </svg>
                        </i>&ensp; <a style="padding-top: 3px !important;"  class="contact-link" target="_blank"  href="mailto:{data}" >{data}</a>
        """
    else:
        return '-'


def get_comments_as_html(comments, me) -> str:
    html: str = ''
    for comment in comments:
        if comment.author == me:
            html += f"""
                <li class="">
                    <div style="text-align: right">
                        <div class=" chat-me">
                            <p>{comment.content}</p>
                            <span>{comment.get_time()}</span>
                        </div>
                    </div>
                </li>
        """
        else:
            html += f"""
            <li class="">
                <div>
                    <div class=" chat-from">
                        <h4 class="c-font-20">{comment.author}</h4>
                        <p>{comment.content}</p>
                        <span>{comment.get_time()}</span>
                    </div>
                </div>
            </li>
            """
    return html


def get_customer_info(profile):
    return f"""
    <div class="col-md-6">
        <ul class="list-unstyled">
            <li>User ID: {profile.customer_id}</li>
            <li>Name: {profile}</li>
            <li>Company Name: {profile.get_company_name}</li>
            <li>Company ID: {profile.get_company_id}</li>
        </ul>
    </div>
    <div class="col-md-6">
        <ul class="list-unstyled">
            <li>Telegram: {profile.get_telegram}</li>
            <li>Email: <a href="mailto:{profile.get_email}"
                          class="c-theme-color">{profile.get_email}</a></li>
            <li>Phone: {profile.get_phone}</li>
        </ul>
    </div>
    """
def draw_stars(rating):
    starts = ''
    whole = rating//1
    rest = rating%1
    for i in range(1, int(whole) + 1):
        starts += f"""<i class="fa fa-star c-font-star"></i>"""
    for i in range(int(whole) + 1, 6):
        starts += f"""<i class="fa fa-star-o c-font-star"></i>"""
    return starts + f"&nbsp<i>{get_data_float(rating)}</i>"
