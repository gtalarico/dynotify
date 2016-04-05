$(document).ready(function() {


	// Fade Alert In
	// $( ".alert" ).hide().slideUp(300)
	$( ".alert" ).css({'opacity': '0', 'margin-top':'-300px'}).animate({'opacity': '1', 'margin-top':'-50px'}, 500,"swing");

	// Fade Alert Out
	$(".alert").delay(5000).css({opacity:1, 'top':'0px'}).animate({opacity:0, 'top':'-100px'}).fadeOut(300);

    // On Click, Fade Panel
    $(".alert").click(function (e) {
    	$(this).stop();
	});

    // $('.alert').on('closed.bs.alert', function () {
      // do something…
    	// console.log('Uguu')
    	// $(this).css({opacity:1, 'margin-top':'0px'}).animate({opacity:0, 'margin-top':'-100px'}).fadeOut(100);
    // })

    // };


    });

  // Activates PopOver
$(function () {
	// Pop OVer Options
});
