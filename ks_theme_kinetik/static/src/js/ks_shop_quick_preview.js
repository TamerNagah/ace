odoo.define('website_product_quick_preview', function(require){
  "use strict";
    //Handling quick preview on the shop page
     var sAnimation = require('website.content.snippets.animation');
     var ajax = require('web.ajax');
     var core = require('web.core');
     var QWeb = core.qweb;
     var OptionalProductsModal = require('sale.OptionalProductsModal');
     var _t = core._t;
     var ch;
     var qweb_modal = ajax.loadXML('/ks_theme_kinetik/static/src/xml/modal.xml',QWeb);
    sAnimation.registry.product_quick_preview_template = sAnimation.Class.extend({
       selector: ".oe_website_sale",
       template: 'product_quick_preview_template',
        events: {
            'click .o_quick_view' : 'ks_onPreviewClick',
        },
        willStart:function(){
                return this._loadModalTemplate();

        },
        _loadModalTemplate:function(){
            return ajax.loadXML('/ks_theme_kinetik/static/src/xml/modal.xml',QWeb);
        },
        start: function () {
            var self = this;
            return this._super();
        },
         //handles the click on the quick preview button on shop page
         ks_onPreviewClick : function(e){
            var ks_self = this;
            var ks_prod = $(e.currentTarget).data()
            var ks_prod_id = ks_prod.productId
            if (!ks_prod_id){
                var ks_prod_id=ks_prod.productTemplateId
                }
            ajax.jsonRpc("/shop/product", 'call', {'product_id':ks_prod_id}).then(function (data_list) {
            if(data_list[1]==0){
            var data=data_list[0];
            var modal_html =  $(QWeb.render('ks_theme_kinetik.products_modal', {}));
            $('.oe_website_sale div:first').append(modal_html);
            $('#product_modal').html(data);
            $('#product_quick_preview_Modal').modal('show');
             $("#product_quick_preview_Modal").modal({
                show: 'true'
            });
            }
            else{
                $(e.currentTarget).parent().find('.a-submit').click()

            }
        }.bind(ks_self));
        }
    });

});