/* <![CDATA[ */

/// Jquery validate newsletter
$('#newsletter_form').submit(function () {

	var action = $(this).attr('action');

	$("#message-newsletter").slideUp(750, function () {
		$('#message-newsletter').hide();

		$('#submit-newsletter')
			.after('<i class="icon-spin4 animate-spin loader"></i>')
			.attr('disabled', 'disabled');

		$.post(action, {
				email_newsletter: $('#email_newsletter').val()
			},
			function (data) {
				document.getElementById('message-newsletter').innerHTML = data;
				$('#message-newsletter').slideDown('slow');
				$('#newsletter_form .loader').fadeOut('slow', function () {
					$(this).remove()
				});
				$('#submit-newsletter').removeAttr('disabled');
				if (data.match('success') != null) $('#newsletter_form').slideUp('slow');

			}
		);

	});
	return false;
});


// Jquery validate form contact
$('#contactform').submit(function () {

	var action = $(this).attr('action');

	$("#message-contact").slideUp(750, function () {
		$('#message-contact').hide();

		$('#submit-contact')
			.after('<i class="icon-spin4 animate-spin loader"></i>')
			.attr('disabled', 'disabled');

		$.post(action, {
				name_contact: $('#name_contact').val(),
				lastname_contact: $('#lastname_contact').val(),
				email_contact: $('#email_contact').val(),
				phone_contact: $('#phone_contact').val(),
				message_contact: $('#message_contact').val(),
				verify_contact: $('#verify_contact').val()
			},
			function (data) {
				document.getElementById('message-contact').innerHTML = data;
				$('#message-contact').slideDown('slow');
				$('#contactform .loader').fadeOut('slow', function () {
					$(this).remove()
				});
				$('#submit-contact').removeAttr('disabled');
				if (data.match('success') != null) $('#contactform').slideUp('slow');

			}
		);

	});
	return false;
});

/// Jquery validate contact form detail page
$('#contact_detail').submit(function () {

	var action = $(this).attr('action');

	$("#message-contact-detail").slideUp(750, function () {
		$('#message-contact-detail').hide();

		$('#submit-contact-detail')
			.after('<i class="icon-spin4 animate-spin loader"></i>')
			.attr('disabled', 'disabled');

		$.post(action, {
				name_detail: $('#name_detail').val(),
				email_detail: $('#email_detail').val(),
				message_detail: $('#message_detail').val(),
				verify_contact_detail: $('#verify_contact_detail').val()
			},
			function (data) {
				document.getElementById('message-contact-detail').innerHTML = data;
				$('#message-contact-detail').slideDown('slow');
				$('#contact_detail .loader').fadeOut('slow', function () {
					$(this).remove()
				});
				$('#submit-contact-detail').removeAttr('disabled');
				if (data.match('success') != null) $('#contact_detail').slideUp('slow');

			}
		);

	});
	return false;
});

/* ]]> */