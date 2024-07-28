(function($){
	$.fn.mapmarker = function(options){
		var opts = $.extend({}, $.fn.mapmarker.defaults, options);

		return this.each(function() {
			// Apply plugin functionality to each element
			var map_element = this;
			addMapMarker(map_element, opts.zoom, opts.center, opts.markers);
		});
	};

	// Set up default values
	var defaultMarkers = {
		"markers": []
	};

	$.fn.mapmarker.defaults = {
		zoom	: 8,
		center	: 'United States',
		markers	: defaultMarkers
	}

	// Main function code here (ref:google map api v3)
	function addMapMarker(map_element, zoom, center, markers){
		//console.log($.fn.mapmarker.defaults['center']);

		//Set center of the Map
		var myOptions = {
		  zoom: zoom,
		  scrollwheel: false,
		  styles:[{"featureType":"water","elementType":"geometry","stylers":[{"color":"#e9e9e9"},{"lightness":17}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#ffffff"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":16}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":21}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#dedede"},{"lightness":21}]},{"elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#ffffff"},{"lightness":16}]},{"elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#333333"},{"lightness":40}]},{"elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#f2f2f2"},{"lightness":19}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#fefefe"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#fefefe"},{"lightness":17},{"weight":1.2}]}],
		  mapTypeControl: false,
		  draggable: true,
		  zoomControl: true,
				zoomControlOptions: {
					style: google.maps.ZoomControlStyle.LARGE,
					position: google.maps.ControlPosition.RIGHT_CENTER
				},
		  mapTypeId: google.maps.MapTypeId.ROADMAP
		}
		var map = new google.maps.Map(map_element, myOptions);
		var geocoder = new google.maps.Geocoder();
		var infowindow = null;
		var baloon_text = "";

		geocoder.geocode( { 'address': center}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				//In this case it creates a marker, but you can get the lat and lng from the location.LatLng
				map.setCenter(results[0].geometry.location);
			}
			else{
				console.log("Geocode was not successful for the following reason: " + status);
			}
		});

		//run the marker JSON loop here
		$.each(markers.markers, function(i, the_marker){
			latitude=the_marker.latitude;
			longitude=the_marker.longitude;
			icon=the_marker.icon;
			var baloon_text=the_marker.baloon_text;

			if(latitude!="" && longitude!=""){
				var marker = new google.maps.Marker({
					map: map, 
					position: new google.maps.LatLng(latitude,longitude),
					animation: google.maps.Animation.DROP,
					icon: icon
				});

			}
		});
	}

})(jQuery);