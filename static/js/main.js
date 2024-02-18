(function ($) {
    "use strict";
    
  
  
      /*==================================================================
      [ Focus Contact2 ]*/
      $('.input100').each(function(){
          $(this).on('blur', function(){
              if($(this).val().trim() != "") {
                  $(this).addClass('has-val');
              }
              else {
                  $(this).removeClass('has-val');
              }
          })    
      })
    
    
      /*==================================================================
      [ Validate ]*/
      var input = $('.validate-input .input100');
  
      $('.validate-form').submit(function(){
          var check = true;
  
          for(var i=0; i<input.length; i++) {
              if(validate(input[i]) == false){
                  showValidate(input[i]);
                  check=false;
              }
          }
  
          return check;
      });
  
  
      $('.validate-form .input100').each(function(){
          $(this).focus(function(){
             hideValidate(this);
          });
      });
  
      function validate (input) {
          if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
              if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                  return false;
              }
          }
          else {
              if($(input).val().trim() == ''){
                  return false;
              }
          }
      }
  
      function showValidate(input) {
          var thisAlert = $(input).parent();
  
          $(thisAlert).addClass('alert-validate');
      }
  
      function hideValidate(input) {
          var thisAlert = $(input).parent();
  
          $(thisAlert).removeClass('alert-validate');
      }

      function dispEditForm(){

      }
  
  
      
      //////////////// Test Validation 
      $("#submitTest").click(function(){
          var i,er=0;
          var os = 'organizational_skill_' ; 
          var ls = 'leadership_skill_'    ;
          var cs = 'communication_skill_'    ; 
          var tms = 'time_management_skill_'  ;    
          var pss = 'problem_solving_skill_'  ;  
          var sms = 'self_management_skill_'  ;    
          var tws = 'team_work_skill_' ;
          var dms = 'decision_making_skill_';
          var scs = 'self_confidence_skill_';
          var cvs = 'creativity_skill_' ;
  
          while(true){
          for (i=1;i<=6;i++){
              var par = 'input[name=' + os + i.toString() + ']';
              if (!($(par).checked)) {
                  alert("Please answer all the questions before proceeding!");
                  er = 1;
                  break;
              }
          }
          if(er) break;
  
          for (i=1;i<=8;i++){
              var par = 'input[name=' + ls + i.toString() + ']';
              if (!($(par).checked)) {
                  alert("Please answer all the questions before proceeding!");
                  er = 1;
                  break;
              }
          }
          if(er) break;
  
          for (i=1;i<=6;i++){
              var par = 'input[name=' + cs + i.toString() + ']';
              if (!($(par).checked)) {
                  alert("Please answer all the questions before proceeding!");
                  er = 1;
                  break;
              }
          }
          if(er) break;
  
          for (i=1;i<=9;i++){
              var par = 'input[name=' + tms + i.toString() + ']';
              if (!($(par).checked)) {
                  alert("Please answer all the questions before proceeding!");
                  er = 1;
                  break;
              }
          }
          if(er) break;
  
          for (i=1;i<=6;i++){
              var par = 'input[name=' + pss + i.toString() + ']';
              if (!($(par).checked)) {
                  alert("Please answer all the questions before proceeding!");
                  er = 1;
                  break;
              }
          }
          if(er) break;
  
          for (i=1;i<=8;i++){
              var par = 'input[name=' + sms + i.toString() + ']';
              if (!($(par).checked)) {
                  alert("Please answer all the questions before proceeding!");
                  er = 1;
                  break;
              }
          }
          if(er) break;
  
          for (i=1;i<=8;i++){
              var par = 'input[name=' + dms + i.toString() + ']';
              if (!($(par).checked)) {
                  alert("Please answer all the questions before proceeding!");
                  er = 1;
                  break;
              }
          }
          if(er) break;
  
          for (i=1;i<=6;i++){
              var par = 'input[name=' + tws + i.toString() + ']';
              if (!($(par).checked)) {
                  alert("Please answer all the questions before proceeding!");
                  er = 1;
                  break;
              }
          }
          if(er) break;
  
          for (i=1;i<=6;i++){
              var par = 'input[name=' + scs + i.toString() + ']';
              if (!($(par).checked)) {
                  alert("Please answer all the questions before proceeding!");
                  er = 1;
                  break;
              }
          }
          if(er) break;
  
          for (i=1;i<=6;i++){
              var par = 'input[name=' + cvs + i.toString() + ']';
              if (!($(par).checked)) {
                  alert("Please answer all the questions before proceeding!");
                  er = 1;
                  break;
              }
          }
          if(er) break;
  
      }
        });
      
  
    })(jQuery);

    $(document).ready(function() {

        $(".toggleEdit").click(function(){
            $(".editForm").toggle( 'slow', function(){
            //    $(".log").text('Toggle Transition Complete');
            
        $(".editFormbutton").toggle('fast');
         });
     });
    
     $('#toggleEdit').click( function(){
        var empstatus = $(this).data('empstatus');
        if(empstatus=='Placed')
            empstatus = 1;
        else if(empstatus=='Looking for job')
            empstatus = 2;
        else if (empstatus=='Going for higher studies')
            empstatus = 3;
        var pack = $(this).data('package');
        var radios = $('input:radio[name=emp_status]');

        radios.filter("[value="+empstatus+"]").prop('checked', true);
        $('#package').val(pack);
    });

     });