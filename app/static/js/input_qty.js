// This button will increment the value
$('.qtyplus').on('click',function (e) {
	e.preventDefault();
	fieldName = $(this).attr('name');
	// Get its current value
	var currentVal = parseInt($('input[name=' + fieldName + ']').val());
	// If is not undefined
	if (!isNaN(currentVal)) {
		// Increment
		$('input[name=' + fieldName + ']').val(currentVal + 1);
	} else {
		// Otherwise put a 0 there
		$('input[name=' + fieldName + ']').val(1);
	}
});

// This button will decrement the value till 0
$('.qtyminus').on('click',function (e) {
	// Stop acting like a button
	e.preventDefault();
	// Get the field name
	fieldName = $(this).attr('name');
	// Get its current value
	var currentVal = parseInt($('input[name=' + fieldName + ']').val());
	// If it isn't undefined or its greater than 0
	if (!isNaN(currentVal) && currentVal > 0) {
		// Decrement one
		$('input[name=' + fieldName + ']').val(currentVal - 1);
	} else {
		// Otherwise put a 0 there
		$('input[name=' + fieldName + ']').val(0);
	}
});

// Guests sum
$('.qtyplus,.qtyminus').on('click', function(e) {
	$("#qty_total").addClass("rotate-x");
    var sum = 0;
    $('.qty').each(function(){
        sum += +$(this).val();
    });
    $('#qty_total').html(sum);
	
});

// Guests sum animation
function remove_rotate() {
	$('#qty_total').removeClass('rotate-x');
}
const qtyTotal = document.querySelector('#qty_total');
qtyTotal.addEventListener("animationend", remove_rotate);