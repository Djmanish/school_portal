
 
$(document).ready(function(){

  
    $('.n_i').keypress(function (e) {
        var regex = new RegExp("^[a-zA-Z ]+$");
        var strigChar = String.fromCharCode(!e.charCode ? e.which : e.charCode);
        if (regex.test(strigChar)) {
            return true;
        }
        alert('Only Characters Allowed !');
        return false
      });

      $('.only_decimal').keypress(function (e) {
        var regex = new RegExp("^[0-9.]+$");
        var strigChar = String.fromCharCode(!e.charCode ? e.which : e.charCode);
        if (regex.test(strigChar)) {
            return true;
        }
        alert('Only Digits are allowed !');
        return false
      });

      $('.positive_number').keypress(function (e) {
        var regex = new RegExp("^[0-9]+$");
        var strigChar = String.fromCharCode(!e.charCode ? e.which : e.charCode);
        if (regex.test(strigChar)) { 
            return true;
        }
        alert('Only Positive Numbers !');
        return false
      });

      
// starting script for last notification view

$('#user_action_iconb').click(function(){
  $.ajax({
    type:'GET',
    url:'/notice/view/time/',
    data:{user_id:$('#user_action_iconb').attr('atval'),
    
    success: function(msg){
      
    }}
})
})
// ending script for last notification view



 // starting Add the following code if you want the name of the file appear on select
 $(".custom-file-input").on("change", function() {
  var fileName = $(this).val().split("\\").pop();
  $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});

// ending Add the following code if you want the name of the file appear on select

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

 

  var specialElementHandlers = {
    "#editor":function(element, renderer){
      return true;
    }
  };

  $("#cmd").click(function(){

    var doc = new jsPDF();

    doc.fromHTML($("#target").html(),15,15,{
      "width":170,
      "elementHandlers":specialElementHandlers
    });
    doc.save("test.pdf")
  })
//result print
  var testDivElement = document.document.getElementById('result');
  function savePDF() {
    var imgData;
    html2canvas($("#myresult"), {
    useCORS: true,
    onrendered: function (canvas) {
    imgData = canvas.toDataURL(
    'image/png');
    var doc = new jsPDF("a4"); // var doc = new jsPDF('l', 'in', [10, 12]); change page size
    doc.addImage(imgData, 'PNG', 10, 10);
    doc.save('ReportCard.pdf');
    
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

// function checkDate() {
//   var selectedText = document.getElementById('datepicker').value;
  
//   var selectedDate = new Date(selectedText);
//   var now = new Date();
//   for selected_date in selectedDate{
//     if (selected_date < now) {
//    alert("Date must be in the future");
//    return false
//   }
//   }
// }
//previous date validation

// ending script for processing , notification and due date

function validations(){
  var value=document.getElementById("showdate").value;
  if (new Date() < new Date(value)) {
      alert("future date");
  }
}
function formatAMPM(date) {
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var ampm = hours >= 12 ? 'pm' : 'am';
  hours = hours % 12; 
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? '0'+minutes : minutes;
  var strTime = hours + ':' + minutes + ' ' + ampm;
  return strTime;
}

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



