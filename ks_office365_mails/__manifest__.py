{
    "name": "Office365 Mails",

    "summary": """
        This app allows you to sync Office 365 mails with Odoo mails and vice-versa.
    """,

    "description": """
            Office365 Inbox Sync Apps
            Office365 Mails Apps
            Office365 Sent Item Syncing Apps
            Office365 Archive syncing Apps
            Mail Messages Sync Apps
            Auto refresh Mail Sync Apps
            Detailed Log mail sync
            User Specific Syncing
            Cron Job Syncing
            Automatic Mails Syncing
            Mails Attachment syncing 
            Office365 Mails
            Folderwise syncing Apps
            365 Apps
            Odoo Office 365 Apps
            Office 365 Apps
            Odoo 365 connector Apps
            Office 365 Mails Apps
            Office 365 connector Apps
            Office 365 Mails sync
            Office 365 Outlook sync Apps
            Office 365 Outlook connector Apps
            Microsoft Office 365 Mails
            Manual sync Apps
            Two-Way Odoo Apps
            Two-Way Mails sync Apps
            Mails Syncing Apps
            Two-Way Syncing Apps
            Mails Connector
            Microsoft 365 Mails Apps
            Microsoft 365 connector Apps
            Best Office 365 Apps
            Top Office 365 Apps
            Best Microsoft 365 Apps
            Best Mails Syncing Apps
            Best Connector Apps
            Best Outlook Syncing Apps
            Office 365 Add on
            Outlook Mails sync
            Odoo Outlook Add on
            Sync Outlook to Odoo
            Two-Way Apps
            Best Two-Way Sync Apps
            Automatic Two-Way sync
    """,

    'author': "Ksolves India Pvt. Ltd.",
    'license': 'OPL-1',
    'currency': 'EUR',
    'price': 100.0,
    'website': "https://www.ksolves.com",
    'maintainer': 'Ksolves India Pvt. Ltd.',
    'category': 'Tools',
    'version': '12.0.1.0.0',
    'support': 'sales@ksolves.com',

    "depends": ['base',
                'mail',
                "ks_office365_base",
                ],

    "data": [
        'security/ks_user_record_rules.xml',
        'views/ks_office365_mails_user_form.xml',
        'static/src/xml/ks_assets.xml',
        'data/ks_mail_cron.xml'
    ],

    "qweb": [
        'static/src/xml/ks_thread.xml',
    ],
    "images": [
        "static/description/banners/banner1.gif",
    ],
}

