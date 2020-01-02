odoo.define('ks_ecommerce_theme.main', function (require) {
    'use strict';
    var ajax = require('web.ajax');

    $(document).ready(function(){

        var ks_head = $("head");
        var $style = $("<style>")
//                    $("#my_cart").remove();
         ajax.jsonRpc("/new_snippets/styles", 'call', {}).then(function (data) {
            _.each(data,function(e){
                $style.append(data.snippets_css);
            });
            ks_head.append($style);
        });
        $("#ex2").slider({});

         // Without JQuery
//                            var slider = new Slider('#ex2', {});

        //Because of this comparision works on homepage
        $('#wrapwrap.homepage main').addClass("oe_structure oe_empty oe_website_sale");
        var pathname = window.location.pathname;
        var parts = pathname.split("/");
        var last_part = parts[parts.length-1];
        //Removing cart page from the payment pages
        if(last_part==="payment" || last_part==="checkout" || last_part==="address" ){
            $("#my_cart_2").remove();
            }

      var owl = $('.ks_multi_image_horizontal');
      var product_length= $('.ks_multi_image_horizontal .ks_active_variant_image').length
      var ks_loop=true;
      if (product_length<5){
            ks_loop=false;
      }
       owl.owlCarousel({
           loop:ks_loop,
           nav:true,
           dots:false,
           items : 5,
           margin:10,
           responsiveClass: true,
           responsive:{
                0:{
                    items: 3,
                    margin:0,
                },
                767: {
                    items: 4,
                },
                1200:{
                    items: 5,
                }
           },
       });

       owl.on('mousewheel', '.owl-stage', function (e) {
           owl.trigger('next.owl');
           e.preventDefault();
       });

    //for vertical slider

       var ks_vs_start = 0;
       var ks_vs_slide = 100;
       var ks_vs_visible_slides = 4;
       var ks_total_slides = $('.ks-vs-list li').length;

       if(typeof(ks_total_slides)  === "undefined" || ks_total_slides == 0) {
            $('.ks-vs-outer').css('display','none');
       }

       if(ks_total_slides < 4 ) {
            $('.ks-vs-inner').css('height',(ks_total_slides * 100));
            ks_vs_visible_slides = ks_total_slides;
       }

       var ks_vs_total = -((ks_total_slides - ks_vs_visible_slides) * ks_vs_slide);


       if($(window).width() > 540 ) {
            $('.ks-vs-btn-next').click(function(){
                   if(!(ks_vs_start == ks_vs_total)) {
                       ks_vs_start = ks_vs_start - ks_vs_slide;
                       $('.ks-vs-list').css('margin-top',(ks_vs_start));
                   }
           });

           $('.ks-vs-btn-prev').click(function(){
                   if(!(ks_vs_start == 0)){
                       ks_vs_start = ks_vs_start + ks_vs_slide;
                       $('.ks-vs-list').css('margin-top',(ks_vs_start));
                   }
            });
       }
       else {
            ks_vs_slide = 80;
            var ks_vs_total = -((ks_total_slides - 3) * ks_vs_slide);

            $('.ks-vs-btn-next').click(function(){
                   if(!(ks_vs_start == ks_vs_total)) {
                       ks_vs_start = ks_vs_start - ks_vs_slide;
                       $('.ks-vs-list').css('margin-left',(ks_vs_start));
                   }
           });

           $('.ks-vs-btn-prev').click(function(){
                   if(!(ks_vs_start == 0)){
                       ks_vs_start = ks_vs_start + ks_vs_slide;
                       $('.ks-vs-list').css('margin-left',(ks_vs_start));
                   }
            });
       }

    });

});

