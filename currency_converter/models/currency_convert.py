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
import odoo.addons.decimal_precision as dp
import datetime



class cust_currency_convert1(models.Model):
    _inherit="account.invoice"
    
    
    other_cur=fields.Many2one('res.currency', string='Other Currency',
        readonly=True, states={'draft': [('readonly', False)]},
        #track_visibility='always'
        )
    

    amnt_other_curr= fields.Float(string='Amount in other currency',
                     store=True,
                     readonly=True )#,compute=' amnt_in_other_curr') 

    
    
    other_cur_rate=fields.Float(string="Currency Exchange Rate" ,store=True, digits=(16,3))
    
    
    
    @api.onchange('other_cur','date_invoice','currency_id')
    @api.depends('other_cur','date_invoice','currency_id')
    def latest_exchange_rate(self):
        #inv_date = self.date_invoice
        latest_rate_wth_respct_inv=[]
        l_date_rate=[]
        
        
        b_curr_rate_list=[]
        b_date_rate=[]
        
        latest_rate_custom={}
        
        b_curnsy=0.0
        other_curnsy=0.0
        
        #com_currency=
        if self.date_invoice and self.other_cur and self.currency_id:
            #if self.env.user.company_id[0].currency_id != self.other_cur: 
                other_cur1=self.env['res.currency'].search([('name','=',self.other_cur.name)])
                b_currency=self.env['res.currency'].search([('name','=',self.currency_id.name)])
                if other_cur1.rate_ids:
                    for l_rate in other_cur1.rate_ids:
                        if l_rate.name <= self.date_invoice:
                            #latest_rate_wth_respct_inv.append((l_rate.rate))
                            l_date_rate.append(l_rate.name)
                            l_date_rate.append(l_rate.rate)
                            latest_rate_wth_respct_inv.append(l_date_rate)
                            l_date_rate=[]
                            
                    if len(latest_rate_wth_respct_inv) >=1:   
                        sorted_latest_rate_wth_respct_inv=sorted(latest_rate_wth_respct_inv , key=lambda x:x[0])        
                    #latest_rate_wth_respct_inv.sort(key=float)
                        latest_rate1=sorted_latest_rate_wth_respct_inv[-1][1] 
                        other_curnsy=latest_rate1
                        #l_rate=latest_rate1
                        #latest_rate_custom['new_rate']=l_rate
                       ####self.other_cur_rate=latest_rate1
                       ####self.update({'other_cur_rate': latest_rate1})
                       
                    else:
                        raise UserError(_('No exchange rate available for this date! '))
                     
                if  b_currency.rate_ids:
                    for l_rate in b_currency.rate_ids:
                        if l_rate.name <= self.date_invoice:
                            #latest_rate_wth_respct_inv.append((l_rate.rate))
                            b_date_rate.append(l_rate.name)
                            b_date_rate.append(l_rate.rate)
                            b_curr_rate_list.append(b_date_rate)
                            b_date_rate=[]
                            
                    if len(b_curr_rate_list) >=1:   
                        sorted_b_rate_list=sorted(b_curr_rate_list , key=lambda x:x[0])        
                    #latest_rate_wth_respct_inv.sort(key=float)
                        latest_rate12= sorted_b_rate_list[-1][1]
                        b_curnsy=latest_rate12
                        #l_rate=latest_rate1
                        #latest_rate_custom['new_rate']=l_rate
                        n_rate=other_curnsy/b_curnsy
                        self.other_cur_rate= n_rate#latest_rate1
                        self.update({'other_cur_rate': n_rate}) 
                    
                    
#             else:    
#                 if self.env.user.company_id[0].currency_id == self.other_cur:
#                     fixed_d_rate=1.000
#                     self.other_cur_rate=fixed_d_rate
#                     self.update({'other_cur_rate': fixed_d_rate})
#                     if self.currency_id:
#                         
#                         if self.currency_id.rate_ids:
#                             for l_rate in  self.currency_id.rate_ids:
#                                 if l_rate.name <= self.date_invoice:
#                                     #latest_rate_wth_respct_inv.append((l_rate.rate))
#                                     l_date_rate.append(l_rate.name)
#                                     l_date_rate.append(l_rate.rate)
#                                     latest_rate_wth_respct_inv.append(l_date_rate)
#                                     l_date_rate=[]
#                                     
#                             if len(latest_rate_wth_respct_inv) >=1:   
#                                 sorted_latest_rate_wth_respct_inv=sorted(latest_rate_wth_respct_inv , key=lambda x:x[0])        
#                             #latest_rate_wth_respct_inv.sort(key=float)
#                                 latest_rate1=sorted_latest_rate_wth_respct_inv[-1][1]
#                                 latest_rate_custom['new_rate']=latest_rate1
#             
#         return  latest_rate_custom           
                
    @api.onchange('other_cur_rate', 'amount_total')
    @api.depends('other_cur_rate', 'amount_total')
    def amnt_in_other_curr(self): 
#        rate12=self.latest_exchange_rate()
        if self.other_cur_rate and self.amount_total:
         
            new_amnt=self.amount_total* self.other_cur_rate
            self.amnt_other_curr=new_amnt
            self.update({'amnt_other_curr': new_amnt})
#             else:
#                 b_rate=1.0/rate12['new_rate'] 
#                 new_amnt=self.amount_total* b_rate
#                 self.amnt_other_curr=new_amnt
#                 self.update({'amnt_other_curr': new_amnt})        
#     @api.one
#     @api.depends('date_invoice', 'currency_id', 'other_cur','amount_total')
#     def amnt_in_other_currency(self):
#          
#         #self.ensure_one()
#         res1=[]
#          
#         latest_rate_wth_respct_inv=[]
#         l_date_rate=[]
#         if self.currency_id and self.other_cur and self.date_invoice and self.amount_total:
#             base_cur=self.currency_id
# #             
#         return res1
     