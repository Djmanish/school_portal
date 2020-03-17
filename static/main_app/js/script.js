

$(document).ready(function(){

    $('.n_i').keypress(function (e) {
        var regex = new RegExp("^[a-zA-Z ]+$");
        var strigChar = String.fromCharCode(!e.charCode ? e.which : e.charCode);
        if (regex.test(strigChar)) {
            
            return true;
        }
        alert('Only Characters Allowed');
        return false
      });
  
  });

  $(document).ready(function () {
    //called when key is pressed in textbox
    $('.n_a').keypress(function (e) {
       //if the letter is not digit then display error and don't type anything
       if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
          //display error message
          $("#errmsg").html("Digits Only").show().fadeOut("slow");
                 return false;
      }
     });
  });