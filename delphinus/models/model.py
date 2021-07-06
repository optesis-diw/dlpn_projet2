from odoo import api, fields, models, _

class OptesisAirport(models.Model):
    _name = "optesis.airport"
    _description = "Aréoport"
    _order = 'name'

    name =  fields.Char('Aréoport')

class OptesisLieu(models.Model):
    _name = "optesis.lieu"
    _description = "Lieu"
    _order = 'name'

    name =  fields.Char('Lieu')

class OptesisLieuLine(models.Model):
    _name = "optesis.lieu.line"
    _description = "Lignes de Lieu"
    _order = 'name'

    lieu_id = fields.Many2one('optesis.lieu', string='lieu')
    name =  fields.Char('Nom')
    partner_id = fields.Many2one('res.partner', string='Mareyeur')

    @api.onchange('lieu_id')
    def onchangelieu(self):
        if self.lieu_id:
            self.name = self.lieu_id.name


class OptesisCollecteurLine(models.Model):
    _name = "optesis.collecteur.line"
    _description = "Lignes de Collecteur"
    _order = 'name'

    collecteur_id = fields.Many2one('res.partner', string='Collecteur')
    name =  fields.Char('Nom')
    partner_id = fields.Many2one('res.partner', string='Mareyeur')

    @api.onchange('collecteur_id')
    def onchangelieu(self):
        if self.collecteur_id:
            self.name = self.collecteur_id.name

class OptesisLta(models.Model):
    _name = "optesis.lta"
    _description = "LTA"
    _order = 'name'

    name =  fields.Char('L.T.A')

class OptesisTransit(models.Model):
    _name = "optesis.transit"
    _description = "Transit"
    _order = 'name'

    name =  fields.Char('Transit')

class OptesisTransformation(models.Model):
    _name = "optesis.transformation"
    _description = "Transformation"
    _order = 'name'

    name =  fields.Char('Transformation')
    
class OptesisTransformation(models.Model):
    _name = "optesis.calibre"
    _description = "Calibre"
    _order = 'name'

    name =  fields.Char('Calibre')
