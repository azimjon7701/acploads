from django.urls import path

from main.auth_view import login_view, register_view, forgot_password_view, logout_view, confirmation_view, \
    profile_page_view, edit_profile_view, password_reset_view, confirm_password_view, terms_view, scammers_list_view, \
    find_users_view, check_company_id
from main.comment_view import comment_post, comment_get, get_current_customer_info, rate_post, rate_get, block_post, \
    get_blocks_count
from main.views import my_researchs, search_delete, \
    home, carrier, shipper, test, post_research, \
    loads_dict, post_load, search, how_it_works, contact_us, about_us, put_research, load_delete, put_load
from main.contact_view import contact_us_form, contact_us_form_footer, contact_us_form_contact_page

urlpatterns = [
    path('', home, name='home'),
    path('how-it-works/',how_it_works, name='how_it_works'),
    path('about-us/',about_us, name='about_us'),
    path('contact-us/',contact_us, name='contact_us'),
    path('test/', test, name='test'),
    path('carrier/', carrier, name='carrier'),
    path('shipper/', shipper, name='shipper'),
    path('my-researchs/', my_researchs, name='my-researchs'),
    path('post-research/', post_research, name='post-research'),
    path('put-research/<int:id>/', put_research, name='put-research'),
    path('search-delete/<int:id>/', search_delete, name='search_delete'),
    path('load-delete/<int:id>/', load_delete, name='search_delete'),
    path('loads/', loads_dict, name='loads'),
    path('post-load/', post_load, name='post-load'),
    path('put-load/<int:id>/', put_load, name='put-load'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('confirmation/<int:user_id>/', confirmation_view, name='confirmation'),
    path('confirm-password/<int:user_id>/', confirm_password_view, name='confirm_password'),
    path('account/',profile_page_view,name="account"),
    path('blocked-users/',scammers_list_view,name="blocked-users"),
    path('find-users/',find_users_view,name="find-users"),
    path('edit_profile/',edit_profile_view,name="edit_profile"),
    path('password_reset/',password_reset_view,name="password_reset"),
    path('forgot-password/', forgot_password_view, name='forgot-password'),
    path('search/<int:search_id>/',search,name='search'),
    path('terms-of-services/',terms_view,name='terms'),
    path('contact-us-form/',contact_us_form,name='contact-us-form'),
    path('contact-us-form_footer/',contact_us_form_footer,name='contact-us-form_footer'),
    path('contact-us-form_contact_page/',contact_us_form_contact_page,name='contact-us-form_contact_page'),
    path('check-company-id/',check_company_id,name='check-company id'),
    path('comment-get/<int:current_owner>/',comment_get,name='comment-get'),
    path('comment-post/',comment_post,name='comment-post'),
    path('get-current-customer-info/<int:current_customer>/',get_current_customer_info,name='get-current-customer-info'),
    path('rate/',rate_post,name='rate-post'),
    path('get-rate/<int:cid>/',rate_get,name='rate-get'),
    path('block/', block_post, name='block-post'),
    path('get-blocks-count/<int:cid>/',get_blocks_count,name='get-blocks-count')
]
