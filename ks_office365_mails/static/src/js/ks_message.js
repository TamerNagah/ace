odoo.define('ks_office365_mails.Message', function (require) {
"use strict";

var AbstractMessage = require('mail.model.AbstractMessage');

var Message = AbstractMessage.include({

        init: function (parent, data, emojis) {
            this._ks_partner_ids = data.partner_ids;
            this._super.apply(this, arguments);
        },

        ks_get_recipient: function () {
            var ks_msg = "";
            if (this._ks_partner_ids.length){
                for (var key in this._ks_partner_ids){
                    ks_msg = ks_msg + this._ks_partner_ids[key][1] + ", ";
                }
            }
            return ks_msg;
        },
    });

    return Message;
});