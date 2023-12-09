import json

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import JsonResponse
from django.shortcuts import render

from main.models import Search, Load, LoadType, Distance
from utils.distance import calc_distance,get_radius
from utils.helpers import get_data_or_none, get_date_or_none, get_as_tg_username, get_time_limit_hour_query, \
    get_data_price, get_data_str


def home(request):
    context = {
        'current_menu': 'home',
        'page_title':'Welcome To The Any Cap Pro'
    }
    if request.GET.get('modal', None) == 'opened':
        context['modal'] = 'opened'
    if request.GET.get('alert', None):
        context['alert'] = True
    return render(request, 'home.html', context=context)


def how_it_works(request):
    context = {
        'current_menu': 'how-it-works',
        'page_title': 'How It Works'
    }
    if request.GET.get('alert', None):
        context['alert'] = True
    return render(request, 'how_it_works.html', context=context)


def about_us(request):
    context={
        'current_menu': 'about-us',
        'page_title':'About Us'
        }
    if request.GET.get('alert', None):
        context['alert'] = True
    return render(request, 'about_us.html', context=context)


def contact_us(request):
    context={
        'current_menu': 'contact-us',
        'page_title':'Contact Us'
    }
    if request.GET.get('alert', None):
        context['alert'] = True
    return render(request, 'contact_us.html', context=context)


@login_required(login_url='login')
def carrier(request):
    types = LoadType.objects.all().order_by('name')
    loads = Load.objects.filter(get_time_limit_hour_query()).order_by('-published_date')
    return render(request, 'carrier.html', context={
        'current_dash': 'carrier',
        'types': types,
        'loads':loads,
        'page_title':'Dashbord | Carrier'
    })


@login_required(login_url='login')
def shipper(request):
    types = LoadType.objects.all().order_by('name')
    return render(request, 'shipper.html', context={
        'current_dash': 'shipper',
        'types': types,
        'page_title':'Dashbord | Shipper'
    })


@login_required
def test(request):
    return render(request, 'results.html')


@login_required
def my_researchs(request):
    searchs = request.user.profile.searches.order_by('-id')
    return JsonResponse(data={"searchs": [{
        "id": search.id,
        "age": search.age,
        "pickup_date": search.pickup_date.strftime('%m/%d') if search.pickup_date else None,
        "pickup_date_for_picker": search.pickup_date.strftime('%Y-%m-%d') if search.pickup_date else None,
        "origin": search.origin,
        "dh_o": search.dh_o,
        "destination": search.destination,
        "dh_d": search.dh_d,
        "distance": search.distance,
        "length": search.length,
        "weight": search.weight,
        "type_id": search.type_id,
        "type": search.type.name if search.type else None,
    } for search in searchs]})


@login_required
def search_delete(request, id):
    try:
        Search.objects.get(id=id).delete()
    except Exception as e:
        print("Delete search exception: ", e)
        return JsonResponse(status=500, data={'error': str(e)})
    return JsonResponse(status=200, data={'message': 'Successfully deleted', 'id': id})


@login_required
def load_delete(request, id):
    try:
        Load.objects.get(id=id).delete()
    except Exception as e:
        print("Delete search exception: ", e)
        return JsonResponse(status=500, data={'error': str(e)})
    return JsonResponse(status=200, data={'message': 'Successfully deleted', 'id': id})


@login_required
def post_research(request):
    try:
        data: dict = json.loads(request.body)
        type_id = get_data_or_none(data.get('type', None))
        type_obj = LoadType.objects.get(id=type_id) if type_id else None
        search = Search.objects.create(
            owner=request.user.profile,
            age=get_data_or_none(data.get('age')),
            pickup_date=get_date_or_none(data.get('pickup_date')),
            origin=data.get('origin'),
            dh_o=get_data_or_none(data.get('dh_o')),
            destination=data.get('destination'),
            dh_d=get_data_or_none(data.get('dh_d')),
            distance=get_data_or_none(data.get('distance')),
            length=get_data_or_none(data.get('length')),
            weight=get_data_or_none(data.get('weight')),
            type=type_obj
        )
        print(type(search.pickup_date))
        return JsonResponse(status=201, data={"search": {
            "id": search.id,
            "age": search.age,
            "pickup_date": search.pickup_date.strftime('%m/%d') if search.pickup_date else None,
            "pickup_date_for_picker": search.pickup_date.strftime('%Y-%m-%d') if search.pickup_date else None,
            "origin": search.origin,
            "dh_o": search.dh_o,
            "destination": search.destination,
            "dh_d": search.dh_d,
            "distance": search.distance,
            "length": search.length,
            "weight": search.weight,
            "type_id": search.type_id,
            "type": search.type.name if search.type else None,
        }})
    except Exception as e:
        print("error:", e)
        return JsonResponse(status=500, data={"error": str(e)})


@login_required
def put_research(request, id):
    try:
        data: dict = json.loads(request.body)
        print("put data:", data)
        type_id = get_data_or_none(data.get('type', None))
        type = LoadType.objects.get(id=type_id) if type_id else None
        search = Search.objects.filter(id=id)[0]
        if search:
            if get_data_or_none(data.get('age', None)):
                search.age = get_data_or_none(data.get('age', None))
            if type:
                search.type = type
            if get_data_or_none(data.get('origin', None)):
                search.origin = get_data_or_none(data.get('origin', None))
            search.pickup_date = get_date_or_none(data.get('pickup_date', ""))
            search.dh_o = get_data_or_none(data.get('dh_o', None))
            search.destination = get_data_or_none(data.get('destination', None))
            search.dh_d = get_data_or_none(data.get('dh_d', None))
            search.distance = get_data_or_none(data.get('distance', None))
            search.length = get_data_or_none(data.get('length', None))
            search.weight = get_data_or_none(data.get('weight', None))
            search.age = get_data_or_none(data.get('age', None))
            search.save()
        return JsonResponse(status=201, data={"search": {
            "id": search.id,
            "age": search.age,
            "pickup_date": search.pickup_date.strftime('%m/%d') if search.pickup_date else None,
            "pickup_date_for_picker": search.pickup_date.strftime('%Y-%m-%d') if search.pickup_date else None,
            "origin": search.origin,
            "dh_o": search.dh_o,
            "destination": search.destination,
            "dh_d": search.dh_d,
            "distance": search.distance,
            "length": search.length,
            "weight": search.weight,
            "type_id": search.type_id,
            "type": search.type.name if search.type else None,
        }})
    except Exception as e:
        print("error:", e)
        return JsonResponse(status=500, data={"error": str(e)})


@login_required
def loads_dict(request):
    loads = request.user.profile.loads.filter(get_time_limit_hour_query()).order_by('-published_date')
    loads_response = [
        {
            'id': load.id,
            'owner': request.user.profile.id,
            'owner_cid': get_data_or_none(request.user.profile.customer_id),
            'owner_status': get_data_or_none(request.user.profile.status),
            'published_date': load.published_date.strftime('%H:%M  %m/%d'),
            'age': load.get_age,
            'pickup_date': load.pickup_date.strftime('%m/%d') if load.pickup_date else None,
            "pickup_date_for_picker": load.pickup_date.strftime('%Y-%m-%d') if load.pickup_date else None,
            'origin': load.origin,
            'dh_o': load.dh_o,
            'destination': load.destination,
            'dh_d': load.dh_d,
            'distance': round(float(load.distance)) if load.distance else None,
            'length': load.length,
            'weight': load.weight,
            "type_id": load.type_id,
            "type": load.type.name if load.type else None,
            "contact": load.contact,
            "contact_type": load.contact_type,
            "comment": load.comment,
            "price_render": get_data_price(load.price),
            "price":load.price,
            "name": load.name,
            "ref_number": get_data_str(load.ref_number)
        } for load in loads
    ]
    return JsonResponse(data={'loads': loads_response})


@login_required
def post_load(request):
    try:
        data: dict = json.loads(request.body)
        type_id = get_data_or_none(data.get('type', None))
        type = LoadType.objects.get(id=type_id) if type_id else None
        load = Load.objects.create(
            owner=request.user.profile,
            pickup_date=get_date_or_none(data.get('pickup_date')),
            origin=data.get('origin'),
            destination=data.get('destination'),
            distance=get_data_or_none(data.get('distance')),
            length=get_data_or_none(data.get('length')),
            weight=get_data_or_none(data.get('weight')),
            type=type,
            contact=get_as_tg_username(get_data_or_none(data.get('contact'))) if get_data_or_none(data.get('contact_type'))=='telegram' else get_data_or_none(data.get('contact')),
            price=get_data_or_none(data.get('price')),
            contact_type=get_data_or_none(data.get('contact_type')),
            comment=get_data_or_none(data.get('comment')),
            name=get_data_or_none(data.get('name')),
            ref_number=get_data_or_none(data.get('ref_number'))
        )

        return JsonResponse(status=201, data={"load": {
            "id": load.id,
            'owner': request.user.profile.id,
            'owner_cid': get_data_or_none(request.user.profile.customer_id),
            'owner_status': get_data_or_none(request.user.profile.status),
            "pickup_date": load.pickup_date.strftime('%m/%d') if load.pickup_date else None,
            "pickup_date_for_picker": load.pickup_date.strftime('%Y-%m-%d') if load.pickup_date else None,
            'age': load.get_age,
            "origin": load.origin,
            "dh_o": load.dh_o,
            "destination": load.destination,
            "dh_d": load.dh_d,
            "distance": round(float(load.distance)) if load.distance else None,
            "length": load.length,
            "weight": load.weight,
            "type_id": load.type_id,
            "type": load.type.name if load.type else None,
            "price": load.price,
            "price_render": get_data_price(load.price),
            "contact": load.contact,
            "contact_type": load.contact_type,
            "comment": load.comment,
            "name": load.name,
            "ref_number": get_data_str(load.ref_number)
        }})
    except Exception as e:
        print("error:", e)
        return JsonResponse(status=500, data={"error": str(e)})


@login_required
def put_load(request, id):
    try:
        data: dict = json.loads(request.body)
        load_data = Load.objects.filter(id=id)
        load = load_data[0]
        type_id = get_data_or_none(data.get('type', None))
        type = LoadType.objects.get(id=type_id) if type_id else None
        if get_data_or_none(data.get('renew', False)):
            if load:
                load.save()
        elif load:
            if get_date_or_none(data.get('pickup_date')):
                load.pickup_date = get_date_or_none(data.get('pickup_date'))
            if get_data_or_none(data.get('origin')):
                load.origin = get_data_or_none(data.get('origin'))
            load.destination = data.get('destination',"")
            load.distance = get_data_or_none(data.get('distance',None))
            load.length = get_data_or_none(data.get('length',None))
            load.weight = get_data_or_none(data.get('weight',None))
            load.type = type
            load.contact = get_as_tg_username(get_data_or_none(data.get('contact'))) if get_data_or_none(data.get('contact_type'))=='telegram' else get_data_or_none(data.get('contact'))
            load.price = get_data_or_none(data.get('price',None))
            load.contact_type = get_data_or_none(data.get('contact_type',None))
            load.comment = get_data_or_none(data.get('comment',None))
            load.name = get_data_or_none(data.get('name',None))
            load.ref_number = get_data_or_none(data.get('ref_number',None))

            load.save()

        return JsonResponse(status=201, data={"load": {
            "id": load.id,
            'owner': request.user.profile.id,
            'owner_cid': get_data_or_none(request.user.profile.customer_id),
            'owner_status': get_data_or_none(request.user.profile.status),
            "pickup_date": load.pickup_date.strftime('%m/%d') if load.pickup_date else None,
            "pickup_date_for_picker": load.pickup_date.strftime('%Y-%m-%d') if load.pickup_date else None,
            'age': load.get_age,
            "origin": load.origin,
            "dh_o": load.dh_o,
            "destination": load.destination,
            "dh_d": load.dh_d,
            "distance": round(float(load.distance)) if load.distance else None,
            "length": load.length,
            "weight": load.weight,
            "type_id": load.type_id,
            "type": load.type.name if load.type else None,
            "price": load.price,
            "price_render": get_data_price(load.price),
            "contact": load.contact,
            "contact_type": load.contact_type,
            "comment": load.comment,
            "name": load.name,
            "ref_number": load.ref_number,
        }})
    except Exception as e:
        print("error:", e)
        return JsonResponse(status=500, data={"error": str(e)})


@login_required
def search(request, search_id):
    result_radiuses: dict = {
        'o': {},
        'd': {}
    }
    if search_id == 0:
        loads = Load.objects.filter(get_time_limit_hour_query()).order_by('-published_date')
    else:
        search = Search.objects.get(id=search_id)
        query = Q()
        if search.age:
            time_than = timezone.now() - timezone.timedelta(hours=search.age)
            query = query & Q(published_date__gte=time_than)
        if search.pickup_date:
            query = query & Q(pickup_date=search.pickup_date)
        if search.type:
            types = LoadType.objects.filter(id=search.type_id)
            type = types[0]
            if type:
                if type.name != "Any":
                    query = query & Q(type_id=search.type_id)
        if search.weight:
            query = query & (Q(weight__lte=search.weight)|Q(weight=None))
        if search.length:
            query = query & (Q(length__lte=search.length)|Q(length=None))
        calc_distance(search_id,query)
        loads, result_radiuses = Load.filtered_by_search_model(search_id,query)
    print('result_radiuses:',result_radiuses)
    loads_response = [
        {
            'id': load.id,
            'customer_id': request.user.profile.customer_id,
            'owner': request.user.profile.id,
            'owner_cid': get_data_or_none(request.user.profile.customer_id),
            'owner_status': get_data_or_none(request.user.profile.status),
            'published_date': load.published_date.strftime('%m/%d'),
            'age': load.get_age,
            'pickup_date': load.pickup_date.strftime('%m/%d') if load.pickup_date else None,
            'origin': load.origin,
            'dh_o': get_radius(search_id=search_id,load_id=load.id,point='o'),
            'destination': load.destination,
            'dh_d': get_radius(search_id=search_id,load_id=load.id,point='d'),
            'distance': round(float(load.distance)) if load.distance else None,
            'length': load.length,
            'weight': load.weight,
            "type_id": load.type_id,
            "type": load.type.name if load.type else None,
            "contact": load.contact,
            "contact_type": load.contact_type,
            "comment": load.comment,
            "price":load.price,
            "price_render": get_data_price(load.price),
            "name": load.name,
            "ref_number": get_data_str(load.ref_number)
        } for load in loads
    ]
    return JsonResponse(data={'loads': loads_response})
