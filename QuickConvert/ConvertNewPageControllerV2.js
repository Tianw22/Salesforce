({  
    SC : function(component, event, helper){        
        var invalidFields = helper.isFormValid(component);
        if(invalidFields.length > 0){
            var toastEvent2 = $A.get("e.force:showToast");
            toastEvent2.setParams({
                "title": "Error!",
                "message": "Required fields need to be input.",
                "type ": "error"
            });

            toastEvent2.fire(); 
        }else{
            helper.update(component);
            helper.ConvertIt(component);
        }     
    },
})
