odoo.define('website_sale.ks_cart_popup', function (require) {
'use strict';

var sAnimations = require('website.content.snippets.animation');
var core = require('web.core');
var default_popup=require('website_sale.cart');
var _t = core._t;

var timeout;
sAnimations.registry.websiteSaleCartLink.include({
    _onMouseEnter: function (ev){
          var self = this;
//        clearTimeout(timeout);
        $(this.selector).not(ev.currentTarget).popover('hide');
//        timeout = setTimeout(function () {
            if (!self.$el.is(':hover') || $('.mycart-popover:visible').length) {
                return;
            }
            $.get("/shop/cart", {
                type: 'popover',
            }).then(function (data) {
                self.$el.data("bs.popover").config.content = data;
                self.$el.popover("show");
                $('.popover').on('mouseleave', function () {
                    self.$el.trigger('mouseleave');
                });
            });
//        }, 0);
    },
     _onMouseLeave: function (ev) {
        var self = this;
        setTimeout(function () {
            if ($('.popover:hover').length) {
                return;
            }
            if (!self.$el.is(':hover')) {
               self.$el.popover('hide');
            }
        }, 50);
    },
});
});
