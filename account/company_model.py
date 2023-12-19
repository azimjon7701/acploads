from django.db import models


class Company(models.Model):
    class EntityTypeEnum(models.TextChoices):
        CARRIER = 'Carrier', 'carrier'
        BROKER = 'Broker', 'broker'
    company_id = models.CharField(max_length=4, unique=True, null=True)
    mc = models.CharField(max_length=30, null=True, blank=True)
    usdot = models.CharField(max_length=30, null=True, blank=True)
    entity_type = models.CharField(max_length=10, choices=EntityTypeEnum.choices, default=EntityTypeEnum.CARRIER)
    name = models.CharField(max_length=200, null=True, blank=True)
    dba_name = models.CharField(max_length=200, null=True, blank=True)
    address1 = models.CharField(max_length=200, null=True, blank=True)
    address2 = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    status = models.BooleanField(default=False, null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=20)
    email = models.CharField(null=True, blank=True, max_length=50)
    credit_score = models.IntegerField(null=True, blank=True, default=0)
    authority = models.FileField(null=True, blank=True)
    w9 = models.FileField(null=True, blank=True)
    insurance = models.FileField(null=True, blank=True)
    other1 = models.FileField(null=True, blank=True)
    other2 = models.FileField(null=True, blank=True)

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

    @property
    def get_company_status(self):
        return '<span style="color: #02dc02">Active</p>' if self.is_active else '<span style="color: gray">Not Active</span>'

    def company_detail_html(self):
        return f'''
            <h3 class="c-font-uppercase c-font-bold">Company</h3>
            <p style="font-size: 23px;" class="c-font-lowercase c-font-bold">
            <span class="c-font-lowercase c-font-bold">Company Name:</span>&nbsp;<span  style="color: #000000">{self.name if self.name else ' - '}</span>
            </p>
            <p style="font-size: 23px;" class="c-font-lowercase c-font-bold">
            <span class="c-font-lowercase c-font-bold">Company ID:</span>&nbsp;<span  style="color: #000000">{self.company_id if self.company_id else ' - '}</span>
            </p>
            <p style="font-size: 23px;" class="c-font-lowercase c-font-bold">
            <span class="c-font-lowercase c-font-bold">Company Status:</span>&nbsp;{self.get_company_status}
            </p>
            '''

    def __str__(self):
        return self.name if self.name else self.company_id

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"


class CompanyEmployee(models.Model):
    company = models.ForeignKey("account.Company", related_name="company_employees", on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False, null=True)
    is_active = models.BooleanField(default=False, null=True)
    employee = models.ForeignKey("account.Profile", related_name="company_employees", on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} is {'' if self.is_active else 'none'} active {'owner' if self.is_owner else 'member'} of {self.company} company"
