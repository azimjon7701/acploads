import json
from account.comment_models import Comment
from account.models import Profile

from django.http import JsonResponse

from utils.helpers import get_comments_as_html, get_customer_info


def comment_get(request,current_owner):
    profile = Profile.objects.filter(id=current_owner).first()
    if profile:
        comments = Comment.objects.filter(profile=profile)
        return JsonResponse(data={"comments":get_comments_as_html(comments,request.user.profile)})


def comment_post(request):
    data: dict = json.loads(request.body)
    new_message, current_owner = data.get('new_message',None), data.get('current_owner',None)
    if new_message and current_owner:
        profile = Profile.objects.filter(id=current_owner).first()
        if profile:
            comment = Comment.objects.create(
                profile=profile,
                author=request.user.profile,
                content=new_message
            )
            print(data)
            return JsonResponse(data={
                'new_message': get_comments_as_html([comment],request.user.profile)
            })

def rate_post(request):
    data: dict = json.loads(request.body)
    profile_id = data.get('profile_id', None)
    company_id = data.get('company_id', None)
    loc = data.get('loc', None)
    los = data.get('los', None)
    ri = data.get('ri', None)
    lofc = data.get('lofc', None)
    sop = data.get('sop', None)
    print(data,request.user.profile.id)
    res = request.user.profile.set_rating(profile_id,loc=loc,los=los,ri=ri,lofc=lofc,sop=sop)
    if res:
        return JsonResponse(data={
            "status":"OK"
        })
    else:
        return JsonResponse(data={
            "status":"BAD"
        })

def block_post(request):
    data: dict = json.loads(request.body)
    profile_id = data.get('profile_id', None)
    company_id = data.get('company_id', None)
    field = data.get('field', None)
    print(data,request.user.profile.id)
    res = request.user.profile.set_block(profile_id,field)
    if res:
        return JsonResponse(data={
            "status":"OK"
        })
    else:
        return JsonResponse(data={
            "status":"BAD"
        })

def get_blocks_count(request,cid):
    cprofile:Profile = Profile.objects.filter(id=cid).first()
    res = cprofile.get_blocks()
    res.update({
        'nc_modal':request.user.profile.get_block_hover_model_content(cprofile,'nc'),
        'ds_modal':request.user.profile.get_block_hover_model_content(cprofile,'ds'),
        'ui_modal':request.user.profile.get_block_hover_model_content(cprofile,'ui'),
        'ff_modal':request.user.profile.get_block_hover_model_content(cprofile,'ff'),
        'np_modal':request.user.profile.get_block_hover_model_content(cprofile,'np'),
    })
    if cprofile:
        return JsonResponse(data=res)
    return JsonResponse(data={'mesage':'Error'})
def rate_get(request,cid):
    cprofile:Profile = Profile.objects.filter(id=cid).first()
    rate_loc_html = request.user.profile.get_rate_loc_html(cprofile)
    rate_los_html = request.user.profile.get_rate_los_html(cprofile)
    rate_ri_html = request.user.profile.get_rate_ri_html(cprofile)
    rate_lofc_html = request.user.profile.get_rate_lofc_html(cprofile)
    rate_sop_html = request.user.profile.get_rate_sop_html(cprofile)
    data:dict = cprofile.get_rating()
    data.update({
        "rate_loc_html":rate_loc_html,
        "rate_los_html":rate_los_html,
        "rate_ri_html":rate_ri_html,
        "rate_lofc_html":rate_lofc_html,
        "rate_sop_html":rate_sop_html,
    })
    return JsonResponse(data=data)


def get_current_customer_info(request,current_customer):
    profile = Profile.objects.filter(id=current_customer).first()
    return JsonResponse(data={
        "customer_info":get_customer_info(profile)
    })