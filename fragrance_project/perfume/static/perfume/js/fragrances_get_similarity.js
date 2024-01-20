$("#selected-id").change(function () {
    $("#search").removeAttr("disabled");
});

function changebutton() {
    var ingr1 = document.getElementById('ingr1-id')
    var ingr2 = document.getElementById('ingr2-id') 
    var testbtn = document.getElementById('test') 
    if (ingr1.value == '-- select 1st option --' || ingr2.value == '-- select 2nd option --') 
    {
        testbtn.disabled = true;
    }
    else {
        testbtn.disabled = false;
    }
}