// Call hideShow when page is loaded
$(document).ready(function(){
    hideShow()
})

// call hideShow when the user clicks on the component_type dropdownlist
$('.remove-form-row').click(function(){
    hideShow()
});

// The jquery function below hides/shows the k_v, DI and length fields depending on the selected component_type 
function hideShow(){
if(document.getElementById('id_component_type').options[document.getElementById('id_component_type').selectedIndex].value == "1")
{
    $('#id_length').parents('p:first').hide();
    $('#id_DI').parents('p:first').hide();
    $('#id_k_v').parents('p:first').show();
}else
{
    $('#id_length').parents('p:first').show();
    $('#id_DI').parents('p:first').show();
    $('#id_k_v').parents('p:first').hide();
}
}
