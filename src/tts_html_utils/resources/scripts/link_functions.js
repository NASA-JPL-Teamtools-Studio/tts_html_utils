/*
Extracted from mm_report_utilities
*/
function linkToSection(section_id) {
    openTab(event,section_id+'Tab')
}
function linkToComponent(component_id,section_id){
    openTab(event, section_id+'Tab')
    element = document.getElementById(component_id+'Component')
    element.scrollIntoView()
    element.classList.add("yellow-flash")
    setTimeout(()=>{element.classList.remove("yellow-flash")},2000)
}