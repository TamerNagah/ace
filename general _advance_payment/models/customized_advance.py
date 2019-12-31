from odoo import api, fields, models,_


class add_field(models.Model):
    
    _inherit="account.journal"
    
    
    adv_pt=fields.Boolean("Against Advance Payment")
    
    
class Paymentexport(models.Model):
    _inherit = "account.payment"
        
    adv_pt1=fields.Boolean("Against Advance Payment")   
    
          
    @api.onchange('payment_type','adv_pt1','partner_type')
    def _onchange_payment_type(self):
        if not self.invoice_ids:
            # Set default partner type for the payment type
            if self.payment_type == 'inbound':
                self.partner_type = 'customer'
            elif self.payment_type == 'outbound':
                self.partner_type = 'supplier'
            else:
                self.partner_type = False
        # Set payment method domain
        res = self._onchange_journal()
        if self.adv_pt1==True:
            if not res.get('domain', {}):
                res['domain'] = {}
            res['domain']['journal_id'] = self.payment_type == 'inbound' and [('at_least_one_inbound', '=', True)] or self.payment_type == 'outbound' and [('at_least_one_outbound', '=', True)] or []
            res['domain']['journal_id'].append(('adv_pt', '=', True))
            return res
        else:
            if not res.get('domain', {}):
                res['domain'] = {}
            res['domain']['journal_id'] = self.payment_type == 'inbound' and [('at_least_one_inbound', '=', True)] or self.payment_type == 'outbound' and [('at_least_one_outbound', '=', True)] or []
            res['domain']['journal_id'].append(('type', 'in', ('bank', 'cash')))
            return res
