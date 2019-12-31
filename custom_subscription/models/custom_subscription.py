from odoo import api, fields, models,_
from odoo import api, fields, models
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from lxml import etree
from odoo.osv.orm import setup_modifiers
import json
import time
from datetime import date
import calendar
from itertools import groupby
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import UserError
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES
from operator import itemgetter
from odoo import models,fields,api
from lxml import etree
from odoo.osv.orm import setup_modifiers
from odoo.tools.safe_eval import safe_eval
from builtins import str
from odoo.addons.resource.models.resource import string_to_datetime
from odoo.tools import format_date
import datetime
from dateutil.relativedelta import relativedelta



class custom_subs_saleOrder(models.Model):
    _inherit="account.invoice"
    
    customer_ref_no=fields.Char(string="Customer Ref No.")
    customer_po_no= fields.Char(string="Customer PO No." )

class cust_subs(models.Model):

    _inherit = "sale.subscription"
    
    customer_ref_no=fields.Char(string="Customer Ref No.")
    customer_po_no= fields.Char(string="Customer PO No." )
    
    subscribed_date=fields.Date(string="Subscription Date")
    
    
    def _prepare_invoice_data(self):
        res=super(cust_subs,self)._prepare_invoice_data()
        res.update({'customer_po_no':self.customer_po_no,
                    'customer_ref_no':self.customer_ref_no})
        return res
         
#         self.ensure_one()
# 
#         if not self.partner_id:
#             raise UserError(_("You must first select a Customer for Subscription %s!") % self.name)
# 
#         if 'force_company' in self.env.context:
#             company = self.env['res.company'].browse(self.env.context['force_company'])
#         else:
#             company = self.company_id
#             self = self.with_context(force_company=company.id, company_id=company.id)
# 
#         fpos_id = self.env['account.fiscal.position'].get_fiscal_position(self.partner_id.id)
#         journal = self.template_id.journal_id or self.env['account.journal'].search([('type', '=', 'sale'), ('company_id', '=', company.id)], limit=1)
#         if not journal:
#             raise UserError(_('Please define a sale journal for the company "%s".') % (company.name or '', ))
# 
#         next_date = fields.Date.from_string(self.recurring_next_date)
#         if not next_date:
#             raise UserError(_('Please define Date of Next Invoice of "%s".') % (self.display_name,))
#         periods = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}
#         end_date = next_date + relativedelta(**{periods[self.recurring_rule_type]: self.recurring_interval})
#         end_date = end_date - relativedelta(days=1)     # remove 1 day as normal people thinks in term of inclusive ranges.
#         addr = self.partner_id.address_get(['delivery', 'invoice'])
# 
#         sale_order = self.env['sale.order'].search([('order_line.subscription_id', 'in', self.ids)], order="id desc", limit=1)
#         return {
#             'account_id': self.partner_id.property_account_receivable_id.id,
#             'type': 'out_invoice',
#             'partner_id': addr['invoice'],
#             'partner_shipping_id': addr['delivery'],
#             'currency_id': self.pricelist_id.currency_id.id,
#             'journal_id': journal.id,
#             'origin': self.code,
#             'fiscal_position_id': fpos_id,
#             'payment_term_id': sale_order.payment_term_id.id if sale_order else self.partner_id.property_payment_term_id.id,
#             'company_id': company.id,
#             'comment': _("This invoice covers the following period: %s - %s") % (format_date(self.env, next_date), format_date(self.env, end_date)),
#             'user_id': self.user_id.id,
#             'date_invoice': self.recurring_next_date,
#         }
    
#     def action_subscription_invoice(self):
#         self.ensure_one()
#         invoices = self.env['account.invoice'].search([('invoice_line_ids.subscription_id', 'in', self.ids)])
#         action = self.env.ref('account.action_invoice_tree1').read()[0]
#         action["context"] = {"create": False}
#         if len(invoices) > 1:
#             action['domain'] = [('id', 'in', invoices.ids)]
#         elif len(invoices) == 1:
#             action['views'] = [(self.env.ref('account.invoice_form').id, 'form')]
#             action['res_id'] = invoices.ids[0]
#         else:
#             action = {'type': 'ir.actions.act_window_close'}
#        return action

class sale_to_subs(models.Model):
    
    _inherit="sale.order"
    
    
    customer_ref_no=fields.Char(string="Customer Ref No.")
    customer_po_no= fields.Char(string="Customer PO No.")
    
    subscribe_dt=fields.Date(string="Subscription Date")
    
    
    
    
#     @api.multi
#     @api.onchange('partner_id')
#     def onchange_partner_id(self):
#         """
#         Update the following fields when the partner is changed:
#         - Pricelist
#         - Payment terms
#         - Invoice address
#         - Delivery address
#         """
#         if not self.partner_id:
#             self.update({
#                 'partner_invoice_id': False,
#                 'partner_shipping_id': False,
#                 'payment_term_id': False,
#                 'fiscal_position_id': False,
#             })
#             return
# 
#         addr = self.partner_id.address_get(['delivery', 'invoice'])
#         values = {
#             'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
#             'payment_term_id': self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
#             'partner_invoice_id': addr['invoice'],
#             'partner_shipping_id': addr['delivery'],
#             'user_id': self.partner_id.user_id.id or self.partner_id.commercial_partner_id.user_id.id or self.env.uid
#         }
#         if self.env['ir.config_parameter'].sudo().get_param('sale.use_sale_note') and self.env.user.company_id.sale_note:
#             values['note'] = self.with_context(lang=self.partner_id.lang).env.user.company_id.sale_note
# 
#         if self.partner_id.team_id:
#             values['team_id'] = self.partner_id.team_id.id
#         self.update(values)
#     
#         if self.partner_id.ref:
#             #return result
#             prtnr_ref=self.partner_id.ref#  
#             self.customer_ref_no=prtnr_ref 
    
    
    
    @api.onchange('partner_id')
    def fill_form_field(self):
        #result = {}
        if self.partner_id.ref:
            #return result
            prtnr_ref=self.partner_id.ref#  
            self.customer_ref_no=prtnr_ref       
# #         self.description = product_lang.display_name+ ' (' +(str(product_lang.length) if product_lang.length else '')+ ' /' +(str(product_lang.width) if product_lang.width else '')+ ')-(' +(str(product_lang.tanah) if product_lang.tanah else '')+'/' +(str(product_lang.banah) if product_lang.banah else '')+ ') -' +(str(product_lang.col.name) if product_lang.col.name else '')+ ' -' +(str(product_lang.b_col.name) if product_lang.b_col.name else '')+ ' -' +(str(product_lang.br_col.name) if product_lang.br_col.name else '')+ ' -' +(str(product_lang.design.name) if product_lang.design.name else '')+ ' -' +(str(product_lang.shapes.name) if product_lang.shapes.name else '')+ '- ' +(str(product_lang.wash_type) if product_lang.wash_type else '')+ ' -' +(str(product_lang.shade_card_no.name) if product_lang.shade_card_no.name else '')+ ' -' +(str(product_lang.col_des) if product_lang.col_des else '')+ ' -' +(str(product_lang.a_length) if product_lang.a_length else '')+ ' /' +(str(product_lang.a_width) if product_lang.a_width else '')+ ' -'+(str(product_lang.collection.name) if product_lang.collection.name else '') +(str(product_lang.silk.name) if product_lang.silk.name else '')+ ' ' 
# #         if product_lang.description_purchase:
# #             self.description += '\n' + product_lang.description_purchase

       

       # return result
    
    
    
    
    @api.multi
    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        journal_id = self.env['account.invoice'].default_get(['journal_id'])['journal_id']
        if not journal_id:
            raise UserError(_('Please define an accounting sales journal for this company.'))
        
        #code
        #for comment note
#         st_date=self.confirmation_date.strftime("%m/%d/%Y")
#         last_date_of_months=calendar.monthrange(self.confirmation_date.year, self.confirmation_date.month)[1]
#         new_dt=self.confirmation_date.replace(day=last_date_of_months)
#         l_date=new_dt.strftime("%m/%d/%Y")
        if (self.subscribe_dt):
            st_date=self.subscribe_dt.strftime("%m/%d/%Y")
            last_date_of_months=calendar.monthrange(self.subscribe_dt.year, self.subscribe_dt.month)[1]
            new_dt=self.subscribe_dt.replace(day=last_date_of_months)
            l_date=new_dt.strftime("%m/%d/%Y")
        #code
        invoice_vals = {
            'name': self.client_order_ref or '',
            'origin': self.name,
            'type': 'out_invoice',
            'account_id': self.partner_invoice_id.property_account_receivable_id.id,
            'partner_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'journal_id': journal_id,
            'currency_id': self.pricelist_id.currency_id.id,
            'comment': self.note,
            #'comment': "This invoice covers the following period: " + st_date+" - "+ l_date,
            'customer_po_no':self.customer_po_no,   #for adding two extra fields data to invoice
            'customer_ref_no':self.customer_ref_no,
            #code
            
            'payment_term_id': self.payment_term_id.id,
            'fiscal_position_id': self.fiscal_position_id.id or self.partner_invoice_id.property_account_position_id.id,
            'company_id': self.company_id.id,
            'user_id': self.user_id and self.user_id.id,
            'team_id': self.team_id.id,
            'transaction_ids': [(6, 0, self.transaction_ids.ids)],
        }
        if self.subscribe_dt:
            invoice_vals['comment']="This invoice covers the following period: " + st_date+" - "+ l_date
            
        return invoice_vals
    
    
#     @api.multi
#     def invoice_line_create(self, invoice_id, qty):
#         """ Create an invoice line. The quantity to invoice can be positive (invoice) or negative (refund).
#             :param invoice_id: integer
#             :param qty: float quantity to invoice
#             :returns recordset of account.invoice.line created
#         """
#         invoice_lines = self.env['account.invoice.line']
#         precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
#         for line in self:
#             if not float_is_zero(qty, precision_digits=precision) or not line.product_id:
#                 vals = line._prepare_invoice_line(qty=qty)
#                 vals.update({'invoice_id': invoice_id, 'sale_line_ids': [(6, 0, [line.id])]})
#                 invoice_lines |= self.env['account.invoice.line'].create(vals)
#         return invoice_lines
    
    
#     @api.multi
#     def action_invoice_create(self, grouped=False, final=False):
#         """
#         Create the invoice associated to the SO.
#         :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
#                         (partner_invoice_id, currency)
#         :param final: if True, refunds will be generated if necessary
#         :returns: list of created invoices
#         """
#         inv_obj = self.env['account.invoice']
#         precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
#         invoices = {}
#         references = {}
#         invoices_origin = {}
#         invoices_name = {}
# 
#         for order in self:
#             group_key = order.id if grouped else (order.partner_invoice_id.id, order.currency_id.id)
# 
#             # We only want to create sections that have at least one invoiceable line
#             pending_section = None
# 
#             for line in order.order_line:
#                 if line.display_type == 'line_section':
#                     pending_section = line
#                     continue
#                 if float_is_zero(line.qty_to_invoice, precision_digits=precision):
#                     continue
#                 if group_key not in invoices:
#                     inv_data = order._prepare_invoice()
#                     invoice = inv_obj.create(inv_data)
#                     references[invoice] = order
#                     invoices[group_key] = invoice
#                     invoices_origin[group_key] = [invoice.origin]
#                     invoices_name[group_key] = [invoice.name]
#                 elif group_key in invoices:
#                     if order.name not in invoices_origin[group_key]:
#                         invoices_origin[group_key].append(order.name)
#                     if order.client_order_ref and order.client_order_ref not in invoices_name[group_key]:
#                         invoices_name[group_key].append(order.client_order_ref)
# 
#                 if line.qty_to_invoice > 0 or (line.qty_to_invoice < 0 and final):
#                     if pending_section:
#                         pending_section.invoice_line_create(invoices[group_key].id, pending_section.qty_to_invoice)
#                         pending_section = None
#                     line.invoice_line_create(invoices[group_key].id, line.qty_to_invoice)
# 
#             if references.get(invoices.get(group_key)):
#                 if order not in references[invoices[group_key]]:
#                     references[invoices[group_key]] |= order
# 
#         for group_key in invoices:
#             invoices[group_key].write({'name': ', '.join(invoices_name[group_key]),
#                                        'origin': ', '.join(invoices_origin[group_key])})
#             sale_orders = references[invoices[group_key]]
#             if len(sale_orders) == 1:
#                 invoices[group_key].reference = sale_orders.reference
# 
#         if not invoices:
#             raise UserError(_('There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.'))
# 
#         for invoice in invoices.values():
#             invoice.compute_taxes()
#             if not invoice.invoice_line_ids:
#                 raise UserError(_('There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.'))
#             # If invoice is negative, do a refund invoice instead
#             if invoice.amount_total < 0:
#                 invoice.type = 'out_refund'
#                 for line in invoice.invoice_line_ids:
#                     line.quantity = -line.quantity
#             # Use additional field helper function (for account extensions)
#             for line in invoice.invoice_line_ids:
#                 line._set_additional_fields(invoice)
#             # Necessary to force computation of taxes. In account_invoice, they are triggered
#             # by onchanges, which are not triggered when doing a create.
#             invoice.compute_taxes()
#             # Idem for partner
#             so_payment_term_id = invoice.payment_term_id.id
#             invoice._onchange_partner_id()
#             # To keep the payment terms set on the SO
#             invoice.payment_term_id = so_payment_term_id
#             invoice.message_post_with_view('mail.message_origin_link',
#                 values={'self': invoice, 'origin': references[invoice]},
#                 subtype_id=self.env.ref('mail.mt_note').id)
#         return [inv.id for inv in invoices.values()]
# 
#     
#     
#     
    def _prepare_subscription_data(self, template):
        """Prepare a dictionary of values to create a subscription from a template."""
        self.ensure_one()
        values = {
            'name': template.name,
            'template_id': template.id,
            'partner_id': self.partner_invoice_id.id,
            'user_id': self.user_id.id,
            'team_id': self.team_id.id,
            'date_start': fields.Date.today(),
            'description': self.note or template.description,
            'pricelist_id': self.pricelist_id.id,
            'company_id': self.company_id.id,
             
            #code
            'customer_po_no':self.customer_po_no,
            #'customer_ref_no':self.partner_invoice_id.ref,
            'customer_ref_no':self.customer_ref_no,
            'subscribed_date':self.subscribe_dt,
            #code
            'analytic_account_id': self.analytic_account_id.id,
            'payment_token_id': self.transaction_ids.get_last_transaction().payment_token_id.id if template.payment_mode in ['validate_send_payment', 'success_payment'] else False
        }
        default_stage = self.env['sale.subscription.stage'].search([('in_progress', '=', True)], limit=1)
        if default_stage:
            values['stage_id'] = default_stage.id
        # compute the next date
        today = datetime.date.today()
        periods = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}
        invoicing_period = relativedelta(**{periods[template.recurring_rule_type]: template.recurring_interval})
        recurring_next_date = today + invoicing_period
         
        start_date_of_month=today.replace(day=1)
        new_recurring_next_date= start_date_of_month + relativedelta(months=1)
        #values['recurring_next_date'] = fields.Date.to_string(recurring_next_date)
        values['recurring_next_date'] = fields.Date.to_string(new_recurring_next_date)
        return values

    
class sale_order_line_to_subs(models.Model):   
     
    _inherit="sale.order.line"
     
    

     
    @api.multi
    def invoice_line_create(self, invoice_id, qty):
        """ Create an invoice line. The quantity to invoice can be positive (invoice) or negative (refund).
            :param invoice_id: integer
            :param qty: float quantity to invoice
            :returns recordset of account.invoice.line created
        """
        invoice_lines = self.env['account.invoice.line']
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for line in self:
            if not float_is_zero(qty, precision_digits=precision) or not line.product_id:
                vals = line._prepare_invoice_line(qty=qty)
                vals.update({'invoice_id': invoice_id, 'sale_line_ids': [(6, 0, [line.id])]})
                if 'subscription_id' not in vals:
                    vals.update({'subscription_id':self.subscription_id.id})
                invoice_lines |= self.env['account.invoice.line'].create(vals)
        return invoice_lines

       
    @api.multi
    def _prepare_invoice_line(self, qty):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.
    
        :param qty: float quantity to invoice
        """
        self.ensure_one()
        res = {}
        account = self.product_id.property_account_income_id or self.product_id.categ_id.property_account_income_categ_id
        new_price =0.0
        #code
#         yr=self.order_id.confirmation_date.year
#         yr_month=self.order_id.confirmation_date.month
#         days_of_month=calendar.monthrange(yr, yr_month)[-1]
#         total_days_for_bill = days_of_month-(self.order_id.confirmation_date.day-1)
#         new_price = round((self.price_unit/days_of_month)*total_days_for_bill)
        if self.order_id.subscribe_dt:  
            yr=self.order_id.subscribe_dt.year
            yr_month=self.order_id.subscribe_dt.month
            days_of_month=calendar.monthrange(yr, yr_month)[-1]
            total_days_for_bill = days_of_month-(self.order_id.subscribe_dt.day-1)
            new_price = round((self.price_unit/days_of_month)*total_days_for_bill) 
          
        #code
            
            
        if not account and self.product_id:
            raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                (self.product_id.name, self.product_id.id, self.product_id.categ_id.name))
    
        fpos = self.order_id.fiscal_position_id or self.order_id.partner_id.property_account_position_id
        if fpos and account:
            account = fpos.map_account(account)
            
            
        #if (self.order_id.invoice_count > 1):
        #if  self.order_id.invoice_ids:       
        res = {
            'name': self.name,
            'sequence': self.sequence,
            'origin': self.order_id.name,
            'account_id': account.id,
            'price_unit': self.price_unit,
            'quantity': qty,
            'discount': self.discount,
            'uom_id': self.product_uom.id,
            'product_id': self.product_id.id or False,
            'invoice_line_tax_ids': [(6, 0, self.tax_id.ids)],
            'account_analytic_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'display_type': self.display_type,
         }
#         else:
#             if not self.order_id.invoice_ids:
#                 res = {
#                     'name': self.name,
#                     'sequence': self.sequence,
#                     'origin': self.order_id.name,
#                     'account_id': account.id,
#                     'price_unit': self.price_unit,
#                     'quantity': qty,
#                     'discount': self.discount,
#                     'uom_id': self.product_uom.id,
#                     'product_id': self.product_id.id or False,
#                     'invoice_line_tax_ids': [(6, 0, self.tax_id.ids)],
#                     'account_analytic_id': self.order_id.analytic_account_id.id,
#                     'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
#                     'display_type': self.display_type,
#                 }
        if (self.order_id.subscribe_dt):
            res['price_unit']=new_price
    #             for ol in self.order_id.order_line:
    #                 ol.subscription_id.update({'invoice_count':1})
                #self.order_id.order_line[0].subscription_id.update({'invoice_count':1})
                        
        return res
#      
#     
#      
#     @api.multi
#     def invoice_line_create(self, invoice_id, qty):
#         """ Create an invoice line. The quantity to invoice can be positive (invoice) or negative (refund).
#             :param invoice_id: integer
#             :param qty: float quantity to invoice
#             :returns recordset of account.invoice.line created
#         """
#         invoice_lines = self.env['account.invoice.line']
#         precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
#         for line in self:
#             if not float_is_zero(qty, precision_digits=precision) or not line.product_id:
#                 vals = line._prepare_invoice_line(qty=qty)
#                 vals.update({'invoice_id': invoice_id, 'sale_line_ids': [(6, 0, [line.id])]})
#                 invoice_lines |= self.env['account.invoice.line'].create(vals)
#         return invoice_lines























