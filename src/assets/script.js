window.dashlyNamespace = Object.assign({}, window.dashlyNamespace, {
    tabulator: {
        printIcon: function (cell, formatterParams, onRendered) {
            console.log("Hi!")
            return "<i class='fa fa-print'></i>";
        },
        fromFreetext: function (term, values) { //search for exact matches
            var matches = [];

            values.forEach(function (value) {
                //value - one of the values from the value property
                if (value === term) {
                    matches.push(value);
                }
            });
            return matches;
        },
    }
    // dateEditor = function(cell, onRendered, success, cancel, editorParams){  
    //     //create and style editor       
    //     var editor = document.createElement("input");

    //     editor.setAttribute("type", "date");

    //     //create and style input
    //     editor.style.padding = "3px";
    //     editor.style.width = "100%";
    //     editor.style.boxSizing = "border-box";

    //     //Set value of editor to the current value of the cell
    //     editor.value = moment(cell.getValue(), "DD/MM/YYYY").format("YYYY-MM-DD")

    //     //set focus on the select box when the editor is selected (timeout allows for editor to be added to DOM)
    //     onRendered(function(){
    //         editor.focus();
    //         editor.style.css = "100%";
    //     });

    //     //when the value has been set, trigger the cell to update
    //     function successFunc(){
    //         success(moment(editor.value, "YYYY-MM-DD").format("DD/MM/YYYY"));
    //     }

    //     editor.addEventListener("change", successFunc);
    //     editor.addEventListener("blur", successFunc);

    //     //return the editor element
    //     return editor;
    // }
});