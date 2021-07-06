from odoo import api, fields, models, _
from num2words import num2words


class AccountMove(models.Model):
    _inherit= "account.move"
    
    line_ids = fields.One2many('account.move.line', 'move_id', string='Journal Items', copy=True, readonly=True,
        states={'draft': [('readonly', False)]})
    
    quantity = fields.Float(string='Poids',default=1.0, related="line_ids.quantity")
    
    quantity_poids_total = fields.Float(string='somme des poids', digits='Product Unit of Measure', compute="_quantity_poids_total")
    
    
    
    @api.onchange('quantity', 'line_ids')
    def _quantity_poids_total(self):
        for rec in self:
            total = sum(rec.line_ids.mapped('quantity'))
            rec.quantity_poids_total = total
        

    agrement = fields.Selection(selection=[('001', '001/92/C'), ('0003', '003/17/CE')], string="Agrément")
    airport = fields.Many2one('optesis.airport', string='Aréoport')
    lta = fields.Char(string='L.T.A')
    transit = fields.Many2one('optesis.transit', string='Transitaire')
    amount_text = fields.Char('Montant en lettres', compute='get_amount_text')

    
    @api.depends('amount_total', 'currency_id')
    def get_amount_text(self):
        number_in_word = num2words(self.amount_total, lang='fr')
        self.amount_text = number_in_word and number_in_word.capitalize()


class AccountMoveLine(models.Model):
    _inherit= "account.move.line"
    
    quantity = fields.Float(string='Poids',
        default=1.0, digits='Product Unit of Measure',
        help="The optional quantity expressed by this line, eg: number of product sold. "
             "The quantity is not a legal requirement but is very useful for some reports.")
    

    nb_colis = fields.Float(string='Nombre de colis')
    agrement = fields.Selection(selection=[('001', '001/92/C'), ('0003', '003/17/CE')], related='move_id.agrement', store=True, copy=False, index=True, readonly=False)
    airport = fields.Many2one('optesis.airport', related='move_id.airport', store=True, copy=False, index=True, readonly=False)
    #lta = fields.Many2one('optesis.lta', related='move_id.lta', store=True, copy=False, index=True, readonly=False)
    transit = fields.Many2one('optesis.transit', related='move_id.transit', store=True, copy=False, index=True, readonly=False)
    transformation = fields.Many2one('optesis.transformation', string='Transformation')
    calibre = fields.Many2one('optesis.calibre', string='Calibre')
    

    
    @api.model
    def _sale_prepare_sale_line_values(self, order, price):
        """ Generate the sale.line creation value from the current move line """
        self.ensure_one()
        last_so_line = self.env['sale.order.line'].search([('order_id', '=', order.id)], order='sequence desc', limit=1)
        last_sequence = last_so_line.sequence + 1 if last_so_line else 100

        fpos = order.fiscal_position_id or order.partner_id.property_account_position_id
        taxes = fpos.map_tax(self.product_id.taxes_id, self.product_id, order.partner_id)

        return {
            'order_id': order.id,
            'name': self.name,
            'sequence': last_sequence,
            'price_unit': price,
            'tax_id': [x.id for x in taxes],
            'discount': 0.0,
            'product_id': self.product_id.id,
            'transformation': self.transformation_id.id,
            'calibre': self.calibre_id.id,
            'product_uom': self.product_uom_id.id,
            'product_uom_qty': 0.0,
            'is_expense': True,
        }
    
    @api.model
    def _prepare_analytic_line(self):
        """ Prepare the values used to create() an account.analytic.line upon validation of an account.move.line having
            an analytic account. This method is intended to be extended in other modules.
            :return list of values to create analytic.line
            :rtype list
        """
        result = []
        for move_line in self:
            amount = (move_line.credit or 0.0) - (move_line.debit or 0.0)
            default_name = move_line.name or (move_line.ref or '/' + ' -- ' + (move_line.partner_id and move_line.partner_id.name or '/'))
            result.append({
                'name': default_name,
                'date': move_line.date,
                'account_id': move_line.analytic_account_id.id,
                'group_id': move_line.analytic_account_id.group_id.id,
                'tag_ids': [(6, 0, move_line._get_analytic_tag_ids())],
                'unit_amount': move_line.quantity,
                'calibre':move_line.calibre,
                'nb_colis':move_line.nb_colis,
                'product_id': move_line.product_id and move_line.product_id.id or False,
                'product_uom_id': move_line.product_uom_id and move_line.product_uom_id.id or False,
                'amount': amount,
                'general_account_id': move_line.account_id.id,
                'ref': move_line.ref,
                'move_id': move_line.id,
                'user_id': move_line.move_id.invoice_user_id.id or self._uid,
                'partner_id': move_line.partner_id.id,
                'company_id': move_line.analytic_account_id.company_id.id or self.env.company.id,
            })
        return result
    @api.model
    def _copy_data_extend_business_fields(self, values):
        # OVERRIDE to copy the 'purchase_line_id' field as well.
        super(AccountMoveLine, self)._copy_data_extend_business_fields(values)
        values['purchase_line_id'] = self.purchase_line_id.id
        calibre = self.purchase_line_id.calibre
    