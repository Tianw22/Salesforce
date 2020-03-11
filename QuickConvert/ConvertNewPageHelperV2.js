({
    update: function(component, event, helper){
        component.find('editForm').submit();
    },
   
    isFormValid: function (component, event, helper) {
    return (component.find('requiredField') || [])
        .filter(function (i) {
            var value = i.get('v.value');
            return !value || value == '' || value.trim().length === 0;
        })
        .map(function (i) {
            return i.get('v.fieldName');
        });
	  },

    ConvertIt : function(component, event, helper) {  
        var action = component.get("c.convertIt");
        action.setParams({"recordId": component.get("v.recordId")});
        action.setCallback(this, function(res) {
        var response = res.getReturnValue();
        var state = action.getState();
        console.log(response);
        if(component.isValid() && state == "SUCCESS"){            
            var toastEvent = $A.get("e.force:showToast");
            toastEvent.setParams({
                "title": "Success!",
                "message": "This Lead has been converted.",
                "type ": "success"
            });

            toastEvent.fire(); 
            $A.get("e.force:refreshView").fire();
            location.reload();
            
         } else if (state == "ERROR") {
            console.log('There was a problem and the state is: '+ action.getState());
         }
      });
      $A.enqueueAction(action); 
    }
})
