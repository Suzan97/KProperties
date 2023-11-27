function initMap() {
  var input = document.getElementById('location-autocomplete');
  var autocomplete = new google.maps.places.Autocomplete(input);

  autocomplete.addListener('place_changed', function () {
    var place = autocomplete.getPlace();
    if (!place.geometry) {
      return;
    }

    var propertyLocation = {
      lat: place.geometry.location.lat(),
      lng: place.geometry.location.lng()
    };

    var map = new google.maps.Map(document.getElementById('property-map'), {
      center: propertyLocation,
      zoom: 15  // Adjust the zoom level as needed
    });

    var marker = new google.maps.Marker({
      position: propertyLocation,
      map: map,
      title: 'Property Location'
    });
  });
}
{/* // Call the initMap function once the Google Maps API is loaded */ }
initMap();
