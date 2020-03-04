

$(document).ready(function(){

    $('.n_i').keypress(function (e) {
        var regex = new RegExp("^[a-zA-Z ]+$");
        var strigChar = String.fromCharCode(!e.charCode ? e.which : e.charCode);
        if (regex.test(strigChar)) {
            
            return true;
        }
        
        return false
      });
  
  });

