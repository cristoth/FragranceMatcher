const addMoreBtn = document.getElementById('add-more')
const totalNewForms = document.getElementById('id_form-TOTAL_FORMS')

addMoreBtn.addEventListener('click', add_new_form)

function add_new_form(args){
    if(event){
        event.preventDefault()
    }
    // now add new empty form element 
    const currentFragranceForms = document.getElementsByClassName('fragrance-form')
    const currentFormCount = currentFragranceForms.length - 1 // + 1
    const formCopyTarget = document.getElementById('fragrance-form-list')
    const copyEmptyFormEl = document.getElementById('empty-form').cloneNode(true)
    copyEmptyFormEl.setAttribute('class', 'fragrance-form')  // nu neaparat
    copyEmptyFormEl.setAttribute('id', 'form-${currentFormCount}')

    const regex = new RegExp('__prefix__', 'g')
    copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(regex, currentFormCount)
    totalNewForms.setAttribute('value', currentFormCount + 1)
    formCopyTarget.append(copyEmptyFormEl)
}
