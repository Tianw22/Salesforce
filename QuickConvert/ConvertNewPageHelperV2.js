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
        var urlEvent = $A.get("e.force:navigateToURL");
        action.setParams({"recordId": component.get("v.recordId")});
        action.setCallback(this, function(res) {
        var response = res.getReturnValue();
        var state = action.getState();
        console.log(response);
        if(component.isValid() && state === "SUCCESS"){            
            var toastEvent = $A.get("e.force:showToast");
            toastEvent.setParams({
                "title": "Success!",
                "message": "This Lead has been converted.",
                "type ": "success"
            });

            toastEvent.fire(); 
            $A.get("e.force:refreshView").fire();
            //location.reload();
            urlEvent.setParams({
      			"url": "https://xxxxxxxxx.lightning.force.com/lightning/r/Contact/"+ response +"/view" // "xxxxxxxxx" stands for org's unique url name.
    		});
    		urlEvent.fire();
            
         } else if (state === "ERROR") { // Get all the error msg, for example validation rule error msg, while running.
             var errors = action.getError();
             var toastEvent2 = $A.get("e.force:showToast");
                if (errors) {
                    if (errors[0] && errors[0].message) {
                        //alert(errors[0].message);
                        toastEvent2.setParams({
                			"title": "Error!",
                			"message": errors[0].message,
                			"type ": "error"
            			});
                        toastEvent2.fire(); 
            			$A.get("e.force:refreshView").fire();
                    }
            	console.log('There was a problem and the state is: '+ action.getState());
         		}
         
        }else if(status === "INCOMPLETE"){
            alert('No response from server or client is offline.');
        }
        });
      $A.enqueueAction(action); 
    }
    
})
