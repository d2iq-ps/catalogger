// Get the value of category name if it changes
$(function() {
    $('[name="cat_category"]').on('focusout', function() {
      $.getJSON('/_set_category', {
        a: $('input[name="cat_category"]').val(),
      });
    });
});

// Get the value of scope if it changes
$(function() {
    $('[name="cat_scope"]').on('focusout', function() {
      $.getJSON('/_set_scope', {
        a: $("#cat_scope option:selected").text(),
      });
    });
});

/*
// Get the value of scope if it changes
$(function() {
    $('[class="upload_trigger"]').on('change', function() {
       $('#image_upload_modal').modal('show'); 
    });
});
*/