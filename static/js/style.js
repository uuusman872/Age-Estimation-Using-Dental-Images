$(document).ready(function() {

    $("select").click(function() {
      var open = $(this).data("isopen");
      if(open) {
        window.location.href = $(this).val()
      }
      //set isopen to opposite so next time when use clicked select box
      //it wont trigger this event
      $(this).data("isopen", !open);
    });

  });
