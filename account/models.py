from django.contrib.auth.models import User

from utils.helpers import get_as_tg_username, draw_stars
from .comment_models import *
from .company_model import *


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telegram = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=30, null=True)
    customer_id = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    # Ratings
    loc = models.FloatField(default=0, null=True)
    los = models.FloatField(default=0, null=True)
    ri = models.FloatField(default=0, null=True)
    lofc = models.FloatField(default=0, null=True)
    sop = models.FloatField(default=0, null=True)
    # Block Counts
    nc_count = models.IntegerField(default=0, null=True, verbose_name='Blocked by field No Communication')
    ds_count = models.IntegerField(default=0, null=True, verbose_name='Blocked by field Dissatisfied Service')
    ui_count = models.IntegerField(default=0, null=True, verbose_name='Blocked by field Unreliable Information')
    ff_count = models.IntegerField(default=0, null=True, verbose_name='Blocked by field Freight Failure')
    np_count = models.IntegerField(default=0, null=True, verbose_name='Blocked by field No Payments')

    def get_member(self):
        company = self.get_own_company
        member = self
        if company:
            member = company
        return member

    def get_avg_rating(self):
        member = self.get_member()
        c = 0
        total = 0
        if member.loc:
            total += member.loc
            c += 1
        if member.los:
            total += member.los
            c += 1
        if member.ri:
            total += member.ri
            c += 1
        if member.lofc:
            total += member.lofc
            c += 1
        if member.sop:
            total += member.sop
            c += 1
        return total / c if c else 0

    def get_rating(self):
        member = self.get_member()
        avg_rating = self.get_avg_rating()
        return {
            "loc_starred": draw_stars(member.loc),
            "los_starred": draw_stars(member.los),
            "ri_starred": draw_stars(member.ri),
            "lofc_starred": draw_stars(member.lofc),
            "sop_starred": draw_stars(member.sop),
            "avg_starred": draw_stars(avg_rating),
            # "loc_value":member.loc,
            # "los_value":member.los,
            # "ri_value":member.ri,
            # "lofc_value":member.lofc,
            # "sop_value":member.sop,
            # "avg_value":avg_rating
        }

    @property
    def get_company(self) -> Company or None:
        try:
            return self.company_employees.first().company if self.company_employees.first().company.is_active and self.company_employees.first().is_active else None
        except Exception as e:
            print('error:', e)
            return None

    @property
    def get_own_company(self) -> Company or None:
        try:
            return self.company_employees.first().company if self.company_employees.first().company.is_active and self.company_employees.first().is_owner else None
        except Exception as e:
            print('error:', e)
            return None

    @property
    def get_company_non_active(self) -> Company or None:
        try:
            return self.company_employees.first().company
        except Exception as e:
            print('error:', e)
            return None

    @property
    def get_company_employee(self) -> Company or None:
        try:
            return self.company_employees.first() if self.company_employees.first() else None
        except Exception as e:
            print('error:', e)
            return None

    @property
    def get_membership_status(self):
        if self.get_company_employee:
            if self.get_company_employee.is_owner:
                return f"""<span style="color: #02dc02">Owner of Company</span>"""
            elif self.get_company_employee.is_active:
                return f"""<span style="color: #02dc02">Active member of Company</span>"""
            else:
                return f"""<span style="color: gray">Not active member of Company</span>"""

    @property
    def get_membership_status_html(self):
        try:
            return f"""
                <p style="font-size: 23px;" class="c-font-lowercase c-font-bold">
                    <span class="c-font-lowercase c-font-bold">Membership:</span>&nbsp;<span
                        style="color: #02dc02">{self.get_membership_status}</span>
                </p>
                """
        except Exception as e:
            print('error:', e)
            return ''

    @property
    def get_your_company_status(self) -> Company or None:
        try:
            return self.company_employees.first().company if self.company_employees.first().company.is_active and self.company_employees.first().is_active else None
        except Exception as e:
            print('error:', e)
            return None

    @property
    def company_is_active(self):
        try:
            return self.get_company.is_active if self.get_company else None
        except Exception as e:
            print('error:', e)
            return None

    @property
    def get_company_name(self):
        try:
            return self.get_company.name if self.get_company.name else '-'
        except Exception as e:
            print('error:', e)
            return '-'

    @property
    def get_company_id(self):
        try:
            return self.get_company.company_id if self.get_company.company_id else '-' if self.get_company else '-'
        except Exception as e:
            print('error:', e)
            return '-'

    @property
    def get_phone(self):
        try:
            return self.get_company.phone if self.get_company.phone else '-'
        except Exception as e:
            print('error:', e)
            return self.phone if self.phone else '-'

    @property
    def get_telegram(self):
        try:
            return get_as_tg_username(self.get_company.telegram) if self.get_company.telegram else '-'
        except Exception as e:
            print('error:', e)
            return get_as_tg_username(self.telegram) if self.telegram else '-'

    @property
    def get_email(self):
        try:
            return self.get_company.email if self.get_company.email else '-'
        except Exception as e:
            print('error:', e)
            return self.user.email if self.user.email else '-'

    def generate_customer_id(self):
        self.customer_id = 10000 + self.id
        self.save()

    def set_rating(self, pid, loc=None, los=None, ri=None, lofc=None, sop=None):
        profile = Profile.objects.filter(id=pid).first()
        if profile:
            user_rate = self.get_or_create_rate(cprofile=profile)
            if user_rate:
                if loc:
                    user_rate.loc = loc
                if los:
                    user_rate.los = los
                if ri:
                    user_rate.ri = ri
                if lofc:
                    user_rate.lofc = lofc
                if sop:
                    user_rate.sop = sop
                user_rate.save()
                user_rate.recalc_rating()
                return True
            else:
                return False
        else:
            return False

    def set_block(self, pid, field=None):
        profile = Profile.objects.filter(id=pid).first()
        if profile:
            user_block = self.get_or_create_block(cprofile=profile)
            if user_block and field:
                return user_block.toggle_block(field)
            return False
        return False


    def get_rate(self, cprofile) -> Rate or None:
        try:
            company = self.get_own_company
            if company:
                author_company = cprofile.get_own_company
                if author_company:
                    user_rate: Rate = company.rates.get(company=author_company)
                else:
                    user_rate: Rate = company.rates.get(profile=cprofile)
                return user_rate
            else:
                author_company = cprofile.get_own_company
                if author_company:
                    user_rate: Rate = self.rates.get(company=author_company)
                else:
                    user_rate: Rate = self.rates.get(profile=cprofile)
                return user_rate
        except Exception as e:
            print('error:', e)
            return None

    def get_block(self, cprofile) -> Rate or None:
        try:
            company = self.get_own_company
            if company:
                author_company = cprofile.get_own_company
                if author_company:
                    user_block: Block = company.blockeds.get(company=author_company)
                else:
                    user_block: Block = company.blockeds.get(profile=cprofile)
                return user_block
            else:
                author_company = cprofile.get_own_company
                if author_company:
                    user_block: Block = self.blockeds.get(company=author_company)
                else:
                    user_block: Block = self.blockeds.get(profile=cprofile)
                return user_block
        except Exception as e:
            print('error:', e)
            return None

    def get_or_create_rate(self, cprofile) -> Rate or None:
        try:
            company = self.get_own_company
            if company:
                author_company = cprofile.get_own_company
                if author_company:
                    user_rate, created = company.rates.get_or_create(company=author_company)
                else:
                    user_rate, created = company.rates.get_or_create(profile=cprofile)
                return user_rate
            else:
                author_company = cprofile.get_own_company
                if author_company:
                    user_rate, created = self.rates.get_or_create(company=author_company)
                else:
                    user_rate, created = self.rates.get_or_create(profile=cprofile)
                return user_rate
        except Exception as e:
            print('error:', e)
            return None

    def get_or_create_block(self, cprofile) -> Rate or None:
        try:
            company = self.get_own_company
            if company:
                own_company = cprofile.get_own_company
                if own_company:
                    user_block, created = company.blockeds.get_or_create(company=own_company)
                else:
                    user_block, created = company.blockeds.get_or_create(profile=cprofile)
                return user_block
            else:
                own_company = cprofile.get_own_company
                if own_company:
                    user_block, created = self.blockeds.get_or_create(company=own_company)
                else:
                    user_block, created = self.blockeds.get_or_create(profile=cprofile)
                return user_block
        except Exception as e:
            print('error:', e)
            return None

    def get_blocks(self):
        member = self.get_member()
        return {
            'nc_count':member.nc_count,
            'ds_count':member.ds_count,
            'ui_count':member.ui_count,
            'ff_count':member.ff_count,
            'np_count':member.np_count
        }

    def get_block_hover_model_content(self,cprofile,field):
        user_block: Block = self.get_block(cprofile)
        field_value = getattr(user_block, field) if user_block else False
        user_blocks = user_block.get_other_blocks() if user_block else []
        blockers:str = ''
        for ub in user_blocks:
            if getattr(ub,field):
                blockers += f"<li>&nbsp;{ub.get_author()}</li>"
        return f"""
        <div>
            <h3 class="c-font-uppercase c-font-22 c-font-bold c-padding-l-10">
                &nbsp;Block &nbsp;&nbsp;
                <button type="button" class="btn btn-danger block-user-btn"
                        data-field="{field}">{'Unblock' if field_value else 'Block'}
                </button>
            </h3>
            <div>
                <ul class="rated-users list-unstyled rating-items-users">
                    {blockers if blockers else f"<li>&nbsp;No blocked</li>"}
                </ul>
            </div>
        </div>
        """

    def get_rate_loc_html(self, cprofile):
        user_rate: Rate = self.get_rate(cprofile)
        starts = ''
        raters = ''
        rating = 0
        if user_rate:
            rating = user_rate.loc
            rates = user_rate.get_other_rates()
            if rates:
                for rate in rates:
                    if rate.valid_rate() and rate.loc:
                        raters += f"""
                                   <li>
                                       <div class="row">
                                           <div class="col-md-7">
                                               &nbsp;{rate.get_author()}
                                           </div>
                                           <div class="col-md-5 c-product-rating c-right">
                                               {draw_stars(rate.loc)}
                                           </div>
                                       </div>
                                   </li>
                               """

        for i in range(1, int(rating) + 1):
            starts += f"""<span class="star-rate fa fa-star c-font-star" data-value="{i}"></span>"""
        for i in range(int(rating) + 1, 6):
            starts += f"""<span class="star-rate fa fa-star-o c-font-star" data-value="{i}"></span>"""

        return f"""
        <div>
            <h3 class="c-font-uppercase c-font-22 c-font-bold c-padding-l-10">
                &nbsp;Your Rate &nbsp;&nbsp;<div
                    style="display: inline-block"
                    class="c-product-rating c-right">
                <div 
                    class="rating-review {'rated' if user_rate else ''}"  
                    data-selected-rate="0"
                    data-user-rate="{user_rate.loc if user_rate else 0}" 
                    data-profile="{self.id}" 
                    data-field="loc">
                        {starts}
                </div>
            </div>
            </h3>
            <div>
                <ul class="rated-users list-unstyled rating-items-users">
                    {raters if raters else 'Not rated'}
                </ul>
            </div>
         </div>
        """

    def get_rate_los_html(self, cprofile):
        user_rate: Rate = self.get_rate(cprofile)
        starts = ''
        raters = ''
        rating = 0
        if user_rate:
            rating = user_rate.los
            rates = user_rate.get_other_rates()
            if rates:
                for rate in rates:
                    if rate.valid_rate() and rate.los:
                        raters += f"""
                                    <li>
                                        <div class="row">
                                            <div class="col-md-7">
                                                &nbsp;{rate.get_author()}
                                            </div>
                                            <div class="col-md-5 c-product-rating c-right">
                                                {draw_stars(rate.los)}
                                            </div>
                                        </div>
                                    </li>
                                """
        for i in range(1, int(rating) + 1):
            starts += f"""<span class="star-rate fa fa-star c-font-star" data-value="{i}"></span>"""
        for i in range(int(rating) + 1, 6):
            starts += f"""<span class="star-rate fa fa-star-o c-font-star" data-value="{i}"></span>"""

        return f"""
        <div>
            <h3 class="c-font-uppercase c-font-22 c-font-bold c-padding-l-10">
                &nbsp;Your Rate &nbsp;&nbsp;<div
                    style="display: inline-block"
                    class="c-product-rating c-right">
                <div 
                    class="rating-review {'rated' if user_rate else ''}"  
                    data-selected-rate="0"
                    data-user-rate="{user_rate.los if user_rate else 0}" 
                    data-profile="{self.id}" 
                    data-field="los">
                        {starts}
                </div>
            </div>
            </h3>
            <div>
                <ul class="rated-users list-unstyled rating-items-users">
                    {raters if raters else 'Not rated'}
                </ul>
            </div>
         </div>
        """

    def get_rate_ri_html(self, cprofile):
        user_rate: Rate = self.get_rate(cprofile)
        starts = ''
        raters = ''
        rating = 0
        if user_rate:
            rating = user_rate.ri
            rates = user_rate.get_other_rates()
            if rates:
                for rate in rates:
                    if rate.valid_rate() and rate.ri:
                        raters += f"""
                                    <li>
                                        <div class="row">
                                            <div class="col-md-7">
                                                &nbsp;{rate.get_author()}
                                            </div>
                                            <div class="col-md-5 c-product-rating c-right">
                                                {draw_stars(rate.ri)}
                                            </div>
                                        </div>
                                    </li>
                                """
        for i in range(1, int(rating) + 1):
            starts += f"""<span class="star-rate fa fa-star c-font-star" data-value="{i}"></span>"""
        for i in range(int(rating) + 1, 6):
            starts += f"""<span class="star-rate fa fa-star-o c-font-star" data-value="{i}"></span>"""

        return f"""
        <div>
            <h3 class="c-font-uppercase c-font-22 c-font-bold c-padding-l-10">
                &nbsp;Your Rate &nbsp;&nbsp;<div
                    style="display: inline-block"
                    class="c-product-rating c-right">
                <div 
                    class="rating-review {'rated' if user_rate else ''}"  
                    data-selected-rate="0"
                    data-user-rate="{user_rate.ri if user_rate else 0}" 
                    data-profile="{self.id}" 
                    data-field="ri">
                        {starts}
                </div>
            </div>
            </h3>
            <div>
                <ul class="rated-users list-unstyled rating-items-users">
                    {raters if raters else 'Not rated'}
                </ul>
            </div>
         </div>
        """

    def get_rate_lofc_html(self, cprofile):
        user_rate: Rate = self.get_rate(cprofile)
        starts = ''
        raters = ''
        rating = 0
        if user_rate:
            rating = user_rate.lofc
            rates = user_rate.get_other_rates()
            if rates:
                for rate in rates:
                    if rate.valid_rate() and rate.lofc:
                        raters += f"""
                                    <li>
                                        <div class="row">
                                            <div class="col-md-7">
                                                &nbsp;{rate.get_author()}
                                            </div>
                                            <div class="col-md-5 c-product-rating c-right">
                                                {draw_stars(rate.lofc)}
                                            </div>
                                        </div>
                                    </li>
                                """
        for i in range(1, int(rating) + 1):
            starts += f"""<span class="star-rate fa fa-star c-font-star" data-value="{i}"></span>"""
        for i in range(int(rating) + 1, 6):
            starts += f"""<span class="star-rate fa fa-star-o c-font-star" data-value="{i}"></span>"""
        return f"""
        <div>
            <h3 class="c-font-uppercase c-font-22 c-font-bold c-padding-l-10">
                &nbsp;Your Rate &nbsp;&nbsp;<div
                    style="display: inline-block"
                    class="c-product-rating c-right">
                <div 
                    class="rating-review {'rated' if user_rate else ''}"  
                    data-selected-rate="0"
                    data-user-rate="{user_rate.lofc if user_rate else 0}" 
                    data-profile="{self.id}" 
                    data-field="lofc">
                        {starts}
                </div>
            </div>
            </h3>
            <div>
                <ul class="rated-users list-unstyled rating-items-users">
                    {raters if raters else 'Not rated'}
                </ul>
            </div>
         </div>
        """

    def get_rate_sop_html(self, cprofile):
        user_rate: Rate = self.get_rate(cprofile)
        starts = ''
        raters = ''
        rating = 0
        if user_rate:
            rating = user_rate.sop
            rates = user_rate.get_other_rates()
            if rates:
                for rate in rates:
                    if rate.valid_rate() and rate.sop:
                        raters += f"""
                                    <li>
                                        <div class="row">
                                            <div class="col-md-7">
                                                &nbsp;{rate.get_author()}
                                            </div>
                                            <div class="col-md-5 c-product-rating c-right">
                                                {draw_stars(rate.sop)}
                                            </div>
                                        </div>
                                    </li>
                                """
        for i in range(1, int(rating) + 1):
            starts += f"""<span class="star-rate fa fa-star c-font-star" data-value="{i}"></span>"""
        for i in range(int(rating) + 1, 6):
            starts += f"""<span class="star-rate fa fa-star-o c-font-star" data-value="{i}"></span>"""
        return f"""
        <div>
            <h3 class="c-font-uppercase c-font-22 c-font-bold c-padding-l-10">
                &nbsp;Your Rate &nbsp;&nbsp;<div
                    style="display: inline-block"
                    class="c-product-rating c-right">
                <div 
                    class="rating-review {'rated' if user_rate else ''}"  
                    data-selected-rate="0"
                    data-user-rate="{user_rate.sop if user_rate else 0}" 
                    data-profile="{self.id}" 
                    data-field="sop">
                        {starts}
                </div>
            </div>
            </h3>
            <div>
                <ul class="rated-users list-unstyled rating-items-users">
                    {raters if raters else 'Not rated'}
                </ul>
            </div>
         </div>
        """

    def __str__(self):
        if self.user.first_name:
            return self.user.first_name
        if self.user.last_name:
            return self.user.last_name
        if self.user.email:
            return self.user.email
        if self.user.username:
            return self.user.username
        return self.user.username


class Verification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField(unique=True)
    expired_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.email if self.user.email else self.code


class ResetVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField()
    expired_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.email if self.user.email else self.code
