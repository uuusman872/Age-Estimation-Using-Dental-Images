(function ($) {

	"use strict";

	// Window Resize Mobile Menu Fix
	mobileNav();


	// Scroll animation init
	window.sr = new scrollReveal();


	// Menu Dropdown Toggle
	if ($('.menu-trigger').length) {
		$(".menu-trigger").on('click', function () {
			$(this).toggleClass('active');
			$('.header-area .nav').slideToggle(200);
		});
	}



	// Home seperator
	if ($('.home-seperator').length) {
		$('.home-seperator .left-item, .home-seperator .right-item').imgfix();
	}


	// Home number counterup
	if ($('.count-item').length) {
		$('.count-item strong').counterUp({
			delay: 10,
			time: 1000
		});
	}


	// Page loading animation
	$(window).on('load', function () {
		if ($('.cover').length) {
			$('.cover').parallax({
				imageSrc: $('.cover').data('image'),
				zIndex: '1'
			});
		}

		$("#preloader").animate({
			'opacity': '0'
		}, 600, function () {
			setTimeout(function () {
				$("#preloader").css("visibility", "hidden").fadeOut();
			}, 300);
		});
	});


	// Window Resize Mobile Menu Fix
	$(window).on('resize', function () {
		mobileNav();
	});


	// Window Resize Mobile Menu Fix
	function mobileNav() {
		var width = $(window).width();
		$('.submenu').on('click', function () {
			if (width < 992) {
				$('.submenu ul').removeClass('active');
				$(this).find('ul').toggleClass('active');
			}
		});
	}
	//     $('#main-menu').metisMenu();

	//     /*====================================
	//       LOAD APPROPRIATE MENU BAR
	//    ======================================*/
	//     $(window).bind("load resize", function () {
	//         if ($(this).width() < 768) {
	//             $('div.sidebar-collapse').addClass('collapse')
	//         } else {
	//             $('div.sidebar-collapse').removeClass('collapse')
	//         }
	//     });

})(window.jQuery);


window.onscroll = function () {
	scrollFunction();

};

function scrollFunction() {
	if (document.body.scrollTop > 150 || document.documentElement.scrollTop > 150) {
		document.getElementById("navbar").style.top = "0px";
		document.getElementById("border-radius").style.borderRadius = "10px";





	} else {
		document.getElementById("navbar").style.top = "40px";
		document.getElementById("border-radius").style.borderRadius = "25px";



	}
}



/*  ==========================================
  SHOW UPLOADED IMAGE
* ========================================== */
function readURL(input) {
	if (input.files && input.files[0]) {
		var reader = new FileReader();

		reader.onload = function (e) {
			$('#imageResult')
				.attr('src', e.target.result);
		};
		reader.readAsDataURL(input.files[0]);
	}
}

$(function () {
	$('#upload').on('change', function () {
		readURL(input);
	});
});

