from django.db import models

BLOCK_FIELDS = ['nc', 'ds', 'ui', 'ff', 'np']


class Comment(models.Model):
    profile = models.ForeignKey("account.Profile", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey("account.Profile", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    likes = models.IntegerField(default=0, null=True, blank=True)
    dislikes = models.IntegerField(default=0, null=True, blank=True)

    def get_time(self):
        m = self.created_at.time().minute
        return f"{self.created_at.time().hour}:{m if len(str(m)) > 1 else f'0{m}'}"


class Rate(models.Model):
    company = models.ForeignKey("account.Company", related_name="ratings", on_delete=models.SET_NULL, null=True)
    author_company = models.ForeignKey("account.Company", related_name="rates", on_delete=models.SET_NULL, null=True)
    profile = models.ForeignKey("account.Profile", related_name="ratings", on_delete=models.SET_NULL, null=True)
    author_profile = models.ForeignKey("account.Profile", related_name="rates", on_delete=models.SET_NULL, null=True)
    loc = models.FloatField(default=0, verbose_name='Level of Communication')
    los = models.FloatField(default=0, verbose_name='Level of Service')
    ri = models.FloatField(default=0, verbose_name='Reliable Information')
    lofc = models.FloatField(default=0, verbose_name='Level of Freight Care')
    sop = models.FloatField(default=0, verbose_name='Speed of Payment')

    def recalc_rating(self):
        member = self.get_rated_member()
        if member:
            rates = self.get_other_rates()
            if rates:
                loc, los, ri, lofc, sop = 0.0, 0.0, 0.0, 0.0, 0.0
                loc_count, los_count, ri_count, lofc_count, sop_count = 0, 0, 0, 0, 0
                for rate in rates:
                    if rate.valid_rate():
                        if rate.loc:
                            loc += rate.loc
                            loc_count += 1
                        if rate.los:
                            los += rate.los
                            los_count += 1
                        if rate.ri:
                            ri += rate.ri
                            ri_count += 1
                        if rate.lofc:
                            lofc += rate.lofc
                            lofc_count += 1
                        if rate.sop:
                            sop += rate.sop
                            sop_count += 1
                print(loc, los, ri, lofc, sop)
                print(member)
                print((loc / loc_count) if loc_count else 0)
                print((los / los_count) if los_count else 0)
                print((ri / ri_count) if ri_count else 0)
                print((lofc / lofc_count) if lofc_count else 0)
                print((sop / sop_count) if sop_count else 0)
                member.loc = (loc / loc_count) if loc_count else 0
                member.los = (los / los_count) if los_count else 0
                member.ri = (ri / ri_count) if ri_count else 0
                member.lofc = (lofc / lofc_count) if lofc_count else 0
                member.sop = (sop / sop_count) if sop_count else 0
                member.save()

    def valid_rate(self):
        if self.author_company or self.author_profile:
            return True
        else:
            return False

    def get_rated_member(self):
        if self.company:
            return self.company
        elif self.profile:
            return self.profile
        else:
            return None

    def get_author(self):
        if self.author_company:
            return self.author_company.__str__()
        elif self.author_profile:
            return self.author_profile.__str__()
        else:
            return 'Undefined'

    def get_other_rates(self):
        if self.company:
            return self.company.ratings.all()
        elif self.profile:
            return self.profile.ratings.all()
        else:
            return []


class ReportComment(models.Model):
    comment = models.ForeignKey("account.Comment", related_name="reports", on_delete=models.CASCADE, null=True)
    author_company = models.ForeignKey("account.Company", related_name="reports", on_delete=models.SET_NULL, null=True)
    author_profile = models.ForeignKey("account.Profile", related_name="reports", on_delete=models.SET_NULL, null=True)
    sc = models.BooleanField(default=False, verbose_name='Sexual comment',
                             help_text='Sexual comment')
    vorc = models.BooleanField(default=False, verbose_name='Violent or repulsive comment',
                               help_text='Violent or repulsive comment')
    hoac = models.BooleanField(default=False, verbose_name='Hateful or abusive content',
                               help_text='Hateful or abusive content')
    hob = models.BooleanField(default=False, verbose_name='Harassment or bullying',
                              help_text='Harassment or bullying')
    hoda = models.BooleanField(default=False, verbose_name='Harmful or dangerous acts',
                               help_text='Harmful or dangerous acts')
    mis = models.BooleanField(default=False, verbose_name='Misinformation',
                              help_text='Misinformation')
    pt = models.BooleanField(default=False, verbose_name='Promotes terrorism',
                             help_text='Promotes terrorism')
    som = models.BooleanField(default=False, verbose_name='Spam or misleading',
                              help_text='Spam or misleading')
    li = models.BooleanField(default=False, verbose_name='Legal issue',
                             help_text='Legal issue')


class Block(models.Model):
    company = models.ForeignKey("account.Company", related_name="blocks", on_delete=models.SET_NULL, null=True)
    author_company = models.ForeignKey("account.Company", related_name="blockeds", on_delete=models.SET_NULL, null=True)
    profile = models.ForeignKey("account.Profile", related_name="blocks", on_delete=models.SET_NULL, null=True)
    author_profile = models.ForeignKey("account.Profile", related_name="blockeds", on_delete=models.SET_NULL, null=True)
    nc = models.BooleanField(default=False, verbose_name='No Communication')
    ds = models.BooleanField(default=False, verbose_name='Dissatisfied Service')
    ui = models.BooleanField(default=False, verbose_name='Unreliable Information')
    ff = models.BooleanField(default=False, verbose_name='Freight Failure')
    np = models.BooleanField(default=False, verbose_name='No Payments')

    def get_author(self):
        if self.author_company:
            return self.author_company.__str__()
        elif self.author_profile:
            return self.author_profile.__str__()
        else:
            return 'Undefined'

    def toggle_block(self, field):
        if field in BLOCK_FIELDS:
            if field == 'nc':
                self.toggle_nc()
            if field == 'ds':
                self.toggle_ds()
            if field == 'ui':
                self.toggle_ui()
            if field == 'ff':
                self.toggle_ff()
            if field == 'np':
                self.toggle_np()
            return True
        else:
            return False

    def toggle_nc(self):
        self.nc = not self.nc
        self.save()
        self.recalc_blocks()

    def toggle_ds(self):
        self.ds = not self.ds
        self.save()
        self.recalc_blocks()

    def toggle_ui(self):
        self.ui = not self.ui
        self.save()
        self.recalc_blocks()

    def toggle_ff(self):
        self.ff = not self.ff
        self.save()
        self.recalc_blocks()

    def toggle_np(self):
        self.np = not self.np
        self.save()
        self.recalc_blocks()

    def get_blocked_member(self):
        if self.company:
            return self.company
        elif self.profile:
            return self.profile
        else:
            return None

    def get_other_blocks(self):
        if self.company:
            return self.company.blocks.all()
        elif self.profile:
            return self.profile.blocks.all()
        else:
            return []

    def valid_block(self):
        if self.author_company or self.author_profile:
            return True
        else:
            return False

    def recalc_blocks(self):
        member = self.get_blocked_member()
        if member:
            blocks = self.get_other_blocks()
            if blocks:
                nc, ds, ui, ff, np = 0, 0, 0, 0, 0
                for block in blocks:
                    if block.valid_block():
                        if block.nc:
                            nc += 1
                        if block.ds:
                            ds += 1
                        if block.ui:
                            ui += 1
                        if block.ff:
                            ff += 1
                        if block.np:
                            np += 1
                print(nc, ds, ui, ff, np)
                member.nc_count = nc
                member.ds_count = ds
                member.ui_count = ui
                member.ff_count = ff
                member.np_count = np
                member.save()

    # def __str__(self):
    #     return ''


class ProfileReaction(models.Model):
    profile = models.ForeignKey("account.Profile", on_delete=models.CASCADE, related_name="reactions")
    author = models.ForeignKey("account.Profile", on_delete=models.CASCADE)
    value = models.BooleanField(null=True, blank=True)


class CommentReaction(models.Model):
    comment = models.ForeignKey("account.Comment", on_delete=models.CASCADE, related_name="user_reactions")
    author = models.ForeignKey("account.Profile", on_delete=models.CASCADE, related_name="comment_reactions")
    value = models.BooleanField(null=True, blank=True)
