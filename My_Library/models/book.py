from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Book(models.Model):
    _name = 'library.book'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Library Books'
    _rec_name = 'title'

    title = fields.Char(required=1)
    publication_date = fields.Date(readonly=1)
    book_stock = fields.Integer('books in stock', required=1)
    image = fields.Image()
    states = fields.Selection([('available', 'Available'), ('not_available', 'Not Available')], default='available')
    author_id = fields.Many2one('library.author')
    update = fields.Integer()
    books_states = fields.Boolean()
    member_id = fields.Many2one('res.partner')
    member_name = fields.Char(related='member_id.name')
    member_image = fields.Binary(related='member_id.image_1920')
    author_img = fields.Image(related='author_id.image')
    user_id = fields.Many2one('res.users', 'User', readonly=1)
    borrow_book_ids = fields.One2many('library.borrow.book', 'book_id')
    nb_book_available = fields.Integer(computed='_compute_nb_book_available', readonly=1)
    category = fields.Selection([('auto_biography', 'Auto Biography'), ('biography', 'Biography'),
                                 ('children_book', 'Children Book'), ('fiction', 'Fiction'), ('adventure', 'Adventure'),
                                 ('educational', 'Educational')])

    @api.constrains('book_stock')
    def _compute_nb_book_available(self):
        for rec in self:
            res = self.env['library.borrow.book'].search_count([('book_id', '=', rec.id)])
            rec.nb_book_available = rec.book_stock - res

    def action_open_authors(self):
        action = self.env['ir.actions.actions']._for_xml_id('My_Library.action_library_author')
        view_id = self.env.ref('My_Library.library_author_view_form').id
        action['res_id'] = self.author_id.id
        action['views'] = [[view_id, 'form']]
        return action

    @api.constrains('nb_book_available')
    def state_available_not_available(self):
        for rec in self:
            if rec.nb_book_available > 0:
                rec.states = 'available'
            else:
                rec.states = 'not_available'


    @api.model_create_multi
    def create(self, vals):
        res = super(Book, self).create(vals)
        res.publication_date = fields.Date.today()
        res.user_id = res.env.uid
        return res

