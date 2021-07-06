from odoo import api, fields, models, _

class Partner(models.Model):
    _inherit = "res.partner"

    lieu_ids = fields.One2many('optesis.lieu.line', 'partner_id', string='Lieux')
    collecteur_line = fields.One2many('optesis.collecteur.line', 'partner_id', string='Lieux')
    is_mareyeur = fields.Boolean(string='Mareyeur', default=False)



            