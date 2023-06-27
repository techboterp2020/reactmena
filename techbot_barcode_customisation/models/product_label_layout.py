from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'

    print_format = fields.Selection(selection_add=[('10x100', '10mm x 100 mm'), ('zpl',)],
                                    ondelete={'10x100': 'set default'})

    def _get_report_data(self):
        product_list = []
        if self.move_line_ids:
            for rec in self.move_line_ids:
                if self.picking_quantity == 'custom':
                    qty_done = 1
                else:
                    qty_done = rec.qty_done
                display_name = rec.product_id.name
                company_name = self.env.company.name
                telephone = self.env.company.phone
                barcode = rec.product_id.barcode
                product_list.append({'display_name': display_name,
                                     'company_name': company_name,
                                     'telephone': telephone,
                                     'qty_done': qty_done,
                                     'barcode': barcode, })
        elif self.product_ids:
            for rec in self.product_ids:
                display_name = rec.name
                company_name = self.env.company.name
                telephone = self.env.company.phone
                barcode = rec.barcode
                product_list.append({'display_name': display_name,
                                     'company_name': company_name,
                                     'telephone': telephone,
                                     'qty_done': 1,
                                     'barcode': barcode, })

        elif self.product_tmpl_ids:
            for rec in self.product_tmpl_ids:
                display_name = rec.name
                company_name = self.env.company.name
                telephone = self.env.company.phone
                barcode = rec.barcode
                product_list.append({'display_name': display_name,
                                     'company_name': company_name,
                                     'telephone': telephone,
                                     'qty_done': 1,
                                     'barcode': barcode, })

        return {'count': self.custom_quantity, 'product_list': product_list}

    def get_company_data(self):
        company = self.env.company
        return {'company_id': company}

    def process(self):
        self.ensure_one()
        xml_id, data = self._prepare_report_data()
        if self.print_format == '10x100':
            data = self._get_report_data()
            xml_id = 'techbot_barcode_customisation.custom_barcode_label_print'
        if not xml_id:
            raise UserError(_('Unable to find report template for %s format', self.print_format))

        report_action = self.env.ref(xml_id).report_action(self, data=data)
        report_action.update({'close_on_report_download': False})
        return report_action
