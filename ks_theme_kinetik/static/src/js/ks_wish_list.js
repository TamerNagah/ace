odoo.define('ks_theme_website_wishlist', function (require) {
    'use strict'
     var ks_WishList = require('website_sale_wishlist.wishlist');
     var sAnimations = require('website.content.snippets.animation');
     sAnimations.registry.ProductWishlist.include({
              _addOrMoveWish: function (e) {
                var $def = this._super(e);
                $('#my_cart_2').removeClass('d-none');
                return $def
             },


              _updateWishlistView: function () {
                 $('#my_wish').show();
                   $('.my_wish_quantity').text(this.wishlistProductIDs.length);
                     }

    });
});
