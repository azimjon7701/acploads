import django.utils.timezone
from django.db import models

from utils.helpers import render_contact_by_type, get_data_str, get_data_price, get_time_limit_hour_query

truck_status_choices = (
    ('FTL', 'FTL'),
    ('LTL', 'LTL'),
    ('BOTH', 'BOTH'),
)

type_operators = (
    ('ALL', 'ALL'),
    ('ANY', 'ANY'),
    ('ONLY', 'ONLY')
)


class LoadTypeCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LoadType(models.Model):
    category = models.ForeignKey(LoadTypeCategory, on_delete=models.CASCADE, related_name='types', null=True,
                                 blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Load(models.Model):
    company = models.ForeignKey("account.Company", on_delete=models.SET_NULL, null=True, related_name="loads")
    owner = models.ForeignKey('account.Profile', on_delete=models.SET_NULL, null=True, related_name='loads')
    name = models.CharField(max_length=255, null=True)
    published_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    pickup_date = models.DateField(null=True)
    age = models.IntegerField(null=True, blank=True)
    dlv_date = models.DateField(null=True)
    origin = models.CharField(max_length=255)
    dh_o = models.FloatField(null=True)
    destination = models.CharField(max_length=255, null=True)
    dh_d = models.FloatField(null=True)
    distance = models.FloatField(null=True)
    length = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    suggested_price = models.FloatField(null=True)
    commodity = models.CharField(max_length=255, null=True, blank=True)
    type_operator = models.CharField(max_length=255, null=True, blank=True, choices=type_operators)
    type = models.ManyToManyField(LoadType, null=True, related_name="related_loads",
                                  blank=True)
    contact = models.CharField(max_length=100, null=True)
    contact_type = models.CharField(max_length=20, null=True)
    comment = models.CharField(max_length=120, null=True)
    ref_number = models.CharField(max_length=120, null=True, blank=True)
    truck_status = models.CharField(max_length=10, choices=truck_status_choices, null=True, blank=True)

    def return_dict(self):
        return {
            'id': self.id,
            'published_date': get_data_str(self.published_date.strftime('%H:%M  %m/%d')),
            'age': self.get_age,
            'pickup_date': self.pickup_date.strftime('%m/%d') if self.pickup_date else "-",
            "pickup_date_for_picker": self.pickup_date.strftime('%Y-%m-%d') if self.pickup_date else "-",
            'origin': get_data_str(self.origin),
            'dh_o': get_data_str(self.dh_o),
            'destination': get_data_str(self.destination),
            'dh_d': get_data_str(self.dh_d),
            'distance': round(float(self.distance)) if self.distance else "-",
            'length': get_data_str(self.length),
            'weight': get_data_str(self.weight),
            "contact": get_data_str(self.contact),
            "contact_type": get_data_str(self.contact_type),
            "contact_rendered": render_contact_by_type(self.contact_type, self.contact),
            "comment": get_data_str(self.comment),
            "price": self.price,
            "price_render": get_data_price(self.price),
            "name": get_data_str(self.name),
            "ref_number": get_data_str(self.ref_number),
        }

    def rendered_contact(self):
        print(self.contact_type, self.contact)
        return render_contact_by_type(self.contact_type, self.contact)

    @classmethod
    def filtered_by_search_model(cls, search_id, query):
        result_radiuses: dict = {
            'o': {},
            'd': {}
        }
        search = Search.objects.get(id=search_id)
        loads = cls.objects.filter(query & get_time_limit_hour_query()).order_by('-published_date')
        filtered_loads: list = []
        # for load in loads:
        #     print(load)
        # filtered_loads.append(load)
        for load in loads:
            if load.origin and search.origin and load.destination and search.destination:
                distance_o = Distance.objects.filter(search_address=search.origin).filter(load_address=load.origin)
                distance_d = Distance.objects.filter(search_address=search.destination).filter(
                    load_address=load.destination)
                d_o = distance_o[0].distance if distance_o else 'none'
                d_d = distance_d[0].distance if distance_d else 'none'
                if d_o != 'none' and d_d != 'none':
                    if d_o <= search.dh_o and d_d <= search.dh_d:
                        result_radiuses['o'][load.id] = d_o
                        result_radiuses['d'][load.id] = d_d
                        filtered_loads.append(load)
            elif load.origin and search.origin and not search.destination:
                distance_o = Distance.objects.filter(search_address=search.origin).filter(load_address=load.origin)
                d_o = distance_o[0].distance if distance_o else 'none'
                if d_o != 'none':
                    if d_o <= search.dh_o:
                        result_radiuses['o'][load.id] = d_o
                        filtered_loads.append(load)
            elif load.destination and search.destination:
                distance_d = Distance.objects.filter(search_address=search.destination).filter(
                    load_address=load.destination)
                d_d = distance_d[0].distance if distance_d else 'none'
                if d_d != 'none':
                    if d_d <= search.dh_d:
                        result_radiuses['d'][load.id] = d_d
                        filtered_loads.append(load)

        return filtered_loads, result_radiuses

    def __str__(self):
        return self.published_date.strftime('%Y/%m/%d %H:%M') + f'- {self.origin} -> {self.destination}'

    @property
    def get_age(self):
        age = django.utils.timezone.now() - self.published_date
        daily_hour = age.days * 24
        hour = age.seconds // 3600
        minute = (age.seconds - hour * 3600) // 60
        daily_hour += hour
        hour = f'0{daily_hour}' if len(str(daily_hour)) < 2 else str(daily_hour)
        minute = f'0{minute}' if len(str(minute)) < 2 else str(minute)
        return '00:00' if age.seconds == 0 else f'{hour}:{minute}'


class Search(models.Model):
    owner = models.ForeignKey("account.Profile", on_delete=models.SET_NULL, null=True, related_name='searches')
    age = models.IntegerField(null=True, blank=True)
    pickup_date = models.DateField(null=True, blank=True)
    origin = models.CharField(max_length=255, null=True, blank=True)
    dh_o = models.FloatField(null=True, blank=True)
    destination = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    dh_d = models.FloatField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    type_operator = models.CharField(max_length=255, null=True, blank=True, choices=type_operators)
    type = models.ManyToManyField(LoadType, null=True, related_name='related_searches',
                                  blank=True)
    truck_status = models.CharField(max_length=10, choices=truck_status_choices, null=True, blank=True)
    notification_status = models.BooleanField(default=False, null=True, blank=True)
    results_count = models.IntegerField(null=True, blank=True, default=0)
    results_data = models.ManyToManyField(Load, null=True, related_name='results',
                                          blank=True)

    def __str__(self):
        if self.origin:
            return self.origin
        return f"search {self.id}"


class Distance(models.Model):
    search_address = models.CharField(max_length=255)
    load_address = models.CharField(max_length=255)
    distance = models.FloatField(null=True)

    def __str__(self):
        return f"{self.search_address} - {self.load_address}  ->   {self.distance}"


class ContactUs(models.Model):
    name = models.CharField(null=True, max_length=200)
    email = models.CharField(null=True, max_length=200)
    phone = models.CharField(null=True, max_length=200)
    comment = models.TextField(null=True, max_length=200)

    def message(self):
        return f'''        Name: {self.name}
        Email: {self.email}
        Phone: {self.phone}
        Message: {self.comment}'''

    def __str__(self):
        return self.message()
