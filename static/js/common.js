let search_form_element_ids = [
    'id_deliver',
    'id_serial__icontains',
    'id_content',
    'id_is_received',
    'id_sender__icontains',
    'id_created_on',
    'id_creator',

    ];

function assign_class_by_id(id, className){
    element = document.getElementById(id);
    element.classList.add(className);
    console.log(element)

}



document.addEventListener('DOMContentLoaded', function(){
        for (let element_id of search_form_element_ids){
            assign_class_by_id(element_id, "form-control");
        }
    } , false);
