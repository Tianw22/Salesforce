({
    doInit: function(cmp, event, helper) {
         var getFields = cmp.get('c.getFieldSetMember');
         getFields.setParams({
                     "objectName" :  "Lead",
                     "fieldSetName" :  "LeadConversionFieldSet"
         });
         getFields.setCallback(this, function(response){
             var state = response.getState();
             if(state === 'SUCCESS'){
                 var fields = response.getReturnValue();
                 console.log('fields',fields);
                 cmp.set('v.fields',fields);
                    
                 }else if(state==='INCOMPLETE'){
                 }else if(state ==='ERROR'){
                     console.log('An error occurred.');
                 }
            });
         
         $A.enqueueAction(getFields);	
    },
    
    SC : function(component, event, helper){
        helper.update(component);
        helper.ConvertIt(component);
    },
})
