from odoo import models, fields, api
from odoo.odoo.tools.safe_eval import datetime
from odoo.exceptions import ValidationError


class Membership(models.Model):
    _name = 'library.membership'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ref'

    membership_type = fields.Selection([('monthly', 'Monthly'), ('semestry', 'Semestry'), ('yearly', 'Yearly')],
                                       default="monthly")
    membership_number = fields.Integer()
    renewal_amount = fields.Integer()
    active = fields.Boolean('Active', default=1)
    states = fields.Selection([('draft', 'Draft'), ('active', 'Active'), ('expired', 'Expired')], default='draft')
    expiry_date = fields.Date()
    expiry_email = fields.Boolean()
    member_id = fields.Many2one('res.partner', required=1)
    ref = fields.Char(default="New", readonly=1)
    membership_number_readonly = fields.Integer()



    @api.onchange('membership_type')
    def _compute_renewal_amount(self):
        renewal_amount_monthly = self.env['ir.config_parameter'].get_param('My_Library.renewal_amount_monthly')
        renewal_amount_semestry = self.env['ir.config_parameter'].get_param('My_Library.renewal_amount_semestry')
        renewal_amount_yearly = self.env['ir.config_parameter'].get_param('My_Library.renewal_amount_yearly')

        member = self.member_id
        for rec in self:
            if member.expiry_date and member.expiry_date > fields.Date.today():
                if rec.membership_type == 'monthly':
                    rec.renewal_amount = renewal_amount_monthly
                    rec.expiry_date = member.expiry_date + datetime.timedelta(days=30)
                    member.expiry_date = rec.expiry_date
                elif rec.membership_type == 'semestry':
                    rec.renewal_amount = renewal_amount_semestry
                    rec.expiry_date = member.expiry_date + datetime.timedelta(days=180)
                    member.expiry_date = rec.expiry_date
                else:
                    rec.renewal_amount = renewal_amount_yearly
                    rec.expiry_date = member.expiry_date + datetime.timedelta(days=360)
                    member.expiry_date = rec.expiry_date
            else:
                if rec.membership_type == 'monthly':
                    rec.renewal_amount = renewal_amount_monthly
                    rec.expiry_date = fields.Date.today() + datetime.timedelta(days=30)
                    member.expiry_date = rec.expiry_date
                elif rec.membership_type == 'semestry':
                    rec.renewal_amount = renewal_amount_semestry
                    rec.expiry_date = fields.Date.today() + datetime.timedelta(days=180)
                    member.expiry_date = rec.expiry_date
                else:
                    rec.renewal_amount = renewal_amount_yearly
                    rec.expiry_date = fields.Date.today() + datetime.timedelta(days=360)
                    member.expiry_date = rec.expiry_date



    # draft lazemha tetna7a
    def membership_states_cron(self):
        memberships = self.search([])
        for rec in memberships:
            if rec.states == 'active' or rec.states == 'draft':
                if fields.Date.today() > rec.expiry_date:
                    rec.states = 'expired'
                    rec.active = False
                    rec.member_id.states = 'terminated'

    def action_renew_membership(self):
        memberships = self.search([])
        count = 0
        for rec in memberships:
            if rec.member_id == self.member_id:
                count += 1
        if count > 1:
            raise ValidationError("This Member Is Already Has A Active Membership")
        else:
            self.states = 'active'
            self.member_id.states = 'active'


    @api.constrains('member_id', 'membership_number')
    def check_member_membership_number(self):
        memberships = self.search([])
        for rec in memberships:
            # if rec.states == 'active':
            if rec.member_id == self.member_id and not (rec.membership_number == self.membership_number):
                raise ValidationError('The Membership Number Is Not Correct!!')
            elif not rec.member_id == self.member_id and rec.membership_number == self.membership_number:
                raise ValidationError('The Membership Number Is Already Exist!!')




    @api.model_create_multi
    def create(self, vals):
        res = super(Membership, self).create(vals)
        memberships = res.search([])

        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('membership-seq')

        return res

        # members = self.env['res.partner'].search([])
        # memberships = res.search([])
        # count = 0

        # for rec in memberships:
        #     if rec.membership_number
        # if res.states == 'expired' :



        #
        # for rec in memberships:
        #     if rec.membership_number == member.membership_number:
        #         count += 1
        # if count > 1:
        #     raise ValidationError('Membership Number Already Exists !')
        # count = 0
        # for rec1 in memberships:
        #     if rec1.member_id == member:
        #         count += 1
        # if count > 1:
        #     raise ValidationError('Member is already have a membership')
        # else:
        #     member.membership_number = res.membership_number
        #     member.expiry_date = res.expiry_date
        #     member.states = 'active'
        #     member.membership_id = res.id
        #     res.membership_number_readonly = 1
        #     return res
