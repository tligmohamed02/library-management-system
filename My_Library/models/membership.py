from odoo import models, fields, api
from odoo.odoo.tools.safe_eval import datetime
from odoo.exceptions import ValidationError


class MembershipWizard(models.Model):
    _name = 'library.membership.wizard'
    _rec_name = 'ref'

    membership_type = fields.Selection([('monthly', 'Monthly'), ('semestry', 'Semestry'), ('yearly', 'Yearly')],
                                       default="monthly")
    membership_number = fields.Integer()
    renewal_amount = fields.Integer()
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
                elif rec.membership_type == 'semestry':
                    rec.renewal_amount = renewal_amount_semestry
                    rec.expiry_date = member.expiry_date + datetime.timedelta(days=180)
                else:
                    rec.renewal_amount = renewal_amount_yearly
                    rec.expiry_date = member.expiry_date + datetime.timedelta(days=360)
            else:
                if rec.membership_type == 'monthly':
                    rec.renewal_amount = renewal_amount_monthly
                    rec.expiry_date = fields.Date.today() + datetime.timedelta(days=30)
                elif rec.membership_type == 'semestry':
                    rec.renewal_amount = renewal_amount_semestry
                    rec.expiry_date = fields.Date.today() + datetime.timedelta(days=180)
                else:
                    rec.renewal_amount = renewal_amount_yearly
                    rec.expiry_date = fields.Date.today() + datetime.timedelta(days=360)

    # def action_renew_membership(self):
    #
    #     member = self.member_id
    #     member.membership_number = self.membership_number
    #     member.expiry_date = self.expiry_date
    #     member.membership_id = self.id
    #     member.states = 'active'
    #

        # member_id = self.env.context.get('active_ids', [])
        # member = self.env['res.partner'].browse(member_id)
        # memberships = self.search([])
        # if member.membership_number:
        #     member.membership_number = self.membership_number
        #     member.expiry_date = self.expiry_date
        #     member.membership_id = self.id
        #     member.states = 'active'
        # else:
        #     for rec in memberships:
        #         if rec.membership_number == member.membership_number:
        #             rec.memb += 1
        #     if rec.memb > 1:
        #         raise ValidationError('Membership Number Already Exists !')
        #     else:
        #         member.membership_number = self.membership_number
        #         member.expiry_date = self.expiry_date
        #         member.states = 'active'
        #         member.membership_id = self.id
        #         self.membs = 1




    @api.model_create_multi
    def create(self, vals):
        res = super(MembershipWizard, self).create(vals)
        member = res.member_id
        members = self.env['res.partner'].search([])
        memberships = res.search([])
        count = 0
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('membership-seq')

        for rec in memberships:
            if rec.membership_number == member.membership_number:
                count += 1
        if count > 1:
            raise ValidationError('Membership Number Already Exists !')
        count = 0
        for rec1 in memberships:
            if rec1.member_id == member:
                count += 1
        if count > 1:
            raise ValidationError('Member is already have a membership')
        else:
            member.membership_number = res.membership_number
            member.expiry_date = res.expiry_date
            member.states = 'active'
            member.membership_id = res.id
            res.membership_number_readonly = 1
            print(member.membership_number)
            return res
