$(document).ready(function() {
    $('#id_property').change(function() {
      var selectedProperty = $(this).find(':selected');
      var propertyName = selectedProperty.data('name');
      var propertySlug = selectedProperty.data('slug');
      
      $('#id_name').val(propertyName);
      $('#id_slug').val(propertySlug);
    });
  });