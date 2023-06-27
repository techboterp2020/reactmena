from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    barcode_logo = fields.Binary(string="Barcode Logo")

