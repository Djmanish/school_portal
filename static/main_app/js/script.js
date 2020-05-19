
 
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

      $('.only_decimal').keypress(function (e) {
        var regex = new RegExp("^[0-9.]+$");
        var strigChar = String.fromCharCode(!e.charCode ? e.which : e.charCode);
        if (regex.test(strigChar)) {
            return true;
        }
        alert('Only Digits are allowed !!!');
        return false
      });

      $('.positive_number').keypress(function (e) {
        var regex = new RegExp("^[0-9]+$");
        var strigChar = String.fromCharCode(!e.charCode ? e.which : e.charCode);
        if (regex.test(strigChar)) { 
            return true;
        }
        alert('Only Positive Numbers !!!');
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


//result print
  var testDivElement = document.getElementById('myresult');
  function savePDF() {
      var imgData;
      html2canvas($("#myresult"), {
          useCORS: true,
          onrendered: function (canvas) {
              imgData = canvas.toDataURL(
                 'image/png');
              var doc = new jsPDF('l', 'in', [10, 12]);
              doc.addImage(imgData, 'PNG', 0,0);
              doc.save('sample-file.pdf');
          }
      });
  }

  
// starting script for processing , notification and due date
$(document).ready(function(){
  $('#dates_submit').click(function(){
  var s_processing_date = $("input[name='processing_date']").val();
  var s_notify_date = $('input[name="notification_date"]').val();
  var s_due_date = $('input[name="due_date"]').val();
  if (s_processing_date >= s_notify_date || s_processing_date>= s_due_date){
    alert('Notification date or Due date can not be before processing date !');
    return false;
  }
  });
});
// ending script for processing , notification and due date


 // Add the following code if you want the name of the file appear on select
 $(".custom-file-input").on("change", function() {
  var fileName = $(this).val().split("\\").pop();
  $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});





$('document').ready(function(){
  
  $('option').mousedown(function(e) {
    e.preventDefault();
    $(this).prop('selected', !$(this).prop('selected'));
    return false;
});
})