$(".slider").slick({

    // normal options...
    // infinite: false,
    autoplay: true,
    // speed:50,
    // centerMode: true,
    centerPadding: '60px',
    slidesToShow: 3,

    // the magic
    responsive: [{
            breakpoint: 1150,
            settings: {
                // arrows: false,
                // centerMode: true,
                // centerPadding: '40px',
                slidesToShow: 2,
            }
        },

        {
            breakpoint: 768,
            settings: {
                // arrows: false,
                // centerMode: true,
                centerPadding: '30px',
                slidesToShow: 1,
            }
        }
    ]
});

// $(document).ready(function () {
//   	$('a').click(function () {
//       var section = $(this).text();
//       var sectionlow = section.toLowerCase();
//       var sectionTop =$('.'+sectionlow).offset().top;
//       $("html, body").animate({
//       	scrollTop: sectionTop
//       }, 600);
//       return false;
//     });
// });
//
// $(document).ready(app)
//
//
//
// $(document).ready(function() {
//     $(".menu_logo_movil_abrir").click(function() {
//         // $(this).toggle();
//         $(".menu").toggle(1000);
//
//     });
//     $(".menu_logo_movil_cerrar").click(function() {
//         // $("p").show();
//         $(".menu").toggle();
//         $(".menu_logo_movil_abrir").toggle();
//     });
// });

// $(document).ready(function() {
//     $('.menu_logo_movil_abrir').click(function() {
//             $('.menu').slideToggle("fast");
// console.log();
//             $(this).slideToggle("fast");
//     });
//     $('.menu_logo_movil_cerrar').click(function(){
//         $('.menu').slideToggle("fast");
//             $(this).slideToggle("fast");
//               $('menu_logo_movil_abrir').slideToggle("fast");
//     });
// });





var App = function() {
    this.view = {
        flag: false,
        menu: $('.menu_logo_movil_abrir'),
        constructor: function() {
            this.toggleMenu();
            this.closeMenu();
            this.scrollTop();
            // this.carousel();
        },
        toggleMenu: function() {
          var button = $('.menu_logo_movil_abrir');
          var close = $('.menu_logo_movil_cerrar');
          button.on('click',function(){
            $('.menu').toggle();
          });
          $('.menu_logo_movil_cerrar').on('click',function(){
            $('.menu').toggle();
          })
        },
        closeMenu: function() {
            var self = this;
            $(document).on('click', function() {
                if (self.flag) {
                    selfs.menu.removeClass('openMenu');
                    self.flag = false;
                }
            })
        },
        carousel: function() {
            $('.bxslider').bxSlider({
                maxSlides: 3,
                auto: true,
                responsive: true,
                speed: 600
            });
        },
        scrollTop: function(){
          $('.jump').click(function () {
                var section = $(this).text();
                var sectionlow = section.toLowerCase();
                if(sectionlow=='aplicativo móvil'){
                  var sectionTop =$('.screenshots').offset().top-30;
                }else{
                  var sectionTop =$('.'+sectionlow).offset().top-30;


                }
              // alert("Hello! I am an alert box!! "+sectionlow);
                // console.log(sectionlow);
                // document.write("section.low +" holi boli MMMMMMMMMMMMMMMMMMMMM");


                $("html, body").animate({
                	scrollTop: sectionTop
                }, 600);
                return false;
              });
        }
    }
    this.view.constructor();
}

$(document).ready(App);
