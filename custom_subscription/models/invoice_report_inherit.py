from odoo import api, fields, models,_
from datetime import datetime
from datetime import date, timedelta
class custom_so_invoice(models.AbstractModel):
    #_inherit="account.invoice"
    
    _inherit = 'report.account.report_invoice_with_payments'
    
 #   def convert_to_afghani_currency(self):
    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name('account.report_invoice_with_payments')
        
        
#         
#         latest_rate_wth_respct_inv=[]
#         l_date_rate=[]
#         
#         self_cur_inv=self.env[report.model].browse(docids)
#         if self_cur_inv.move_id:
#             inv_date = self_cur_inv.date_invoice
#             current_currency=self.env['res.currency'].search([('name','=','AFN')]).rate_ids
#             
#             for l_rate in current_currency:
#                 if l_rate.name <= inv_date:
#                     #latest_rate_wth_respct_inv.append((l_rate.rate))
#                     l_date_rate.append(l_rate.name)
#                     l_date_rate.append(l_rate.rate)
#                     latest_rate_wth_respct_inv.append(l_date_rate)
#                     l_date_rate=[]
#                     
#             sorted_latest_rate_wth_respct_inv=sorted(latest_rate_wth_respct_inv , key=lambda x:x[0])        
#             #latest_rate_wth_respct_inv.sort(key=float)
#             latest_rate1=sorted_latest_rate_wth_respct_inv[-1][1] #latest_rate_wth_respct_inv[-1]       
#             afn_amount= latest_rate1* self_cur_inv.amount_total
#         afg_total=0
#         if afn_amount:    
#             afg_total= afn_amount
#             
        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(docids),
            #'afn_total':afn_amount if afn_amount else '',
            'report_type': data.get('report_type') if data else '',
        }   