from odoo import models, fields, api


class Authors(models.Model):
    _name = 'library.author'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Book Author'

    name = fields.Char(required=True)
    biography = fields.Text()
    books_written = fields.One2many('library.book', 'author_id')
    image = fields.Image()
    number_books = fields.Integer('Nombre of books written', compute='_compute_number_books', store=1)




    @api.depends('books_written')
    def _compute_number_books(self):
        for rec in self:
            rec.number_books = self.env['library.book'].search_count([('author_id', '=', rec.id)])




