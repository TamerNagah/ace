{

    'name': 'custom subscription',
    'description': 'custom subscription',
    'author': 'ITech Resources',
    'wesbite': 'www.itechresources.com',
    'depends':
        [
            'base',
            'purchase',
            'sale',
            'account',
            'product',
            'stock',
            'sale_subscription'
        ],
    'data':
        [
            #'security/shafi_access_rights_workflow.xml',
            'views/custom_subscription.xml',
            'views/sale_invoice_report_inherit.xml',
            
        ],
    'installable': True,

}