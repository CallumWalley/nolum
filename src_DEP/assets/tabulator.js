// window.myNamespace = Object.assign({}, window.myNamespace, {
//     tabulator: {
//         dateEditor = function(cell, onRendered, success, cancel, editorParams){  
//             //create and style editor       
//             var editor = document.createElement("input");
        
//             editor.setAttribute("type", "date");
        
//             //create and style input
//             editor.style.padding = "3px";
//             editor.style.width = "100%";
//             editor.style.boxSizing = "border-box";
        
//             //Set value of editor to the current value of the cell
//             editor.value = moment(cell.getValue(), "DD/MM/YYYY").format("YYYY-MM-DD")
        
//             //set focus on the select box when the editor is selected (timeout allows for editor to be added to DOM)
//             onRendered(function(){
//                 editor.focus();
//                 editor.style.css = "100%";
//             });
        
//             //when the value has been set, trigger the cell to update
//             function successFunc(){
//                 success(moment(editor.value, "YYYY-MM-DD").format("DD/MM/YYYY"));
//             }
        
//             editor.addEventListener("change", successFunc);
//             editor.addEventListener("blur", successFunc);
        
//             //return the editor element
//             return editor;
//         },
//         printIcon: function (cell, formatterParams, onRendered) {
//             return "<i class='fa fa-print'></i>";
//         },
//         columnResized : function (column, table) {
//             console.log("Column is resized");
//             console.log(column);
//             console.log(column._column.field)
            
//             // send data back to dash, still under work, only updates when state changes
//             // be aware of table rendering and resetting back to original display
//             //table.props.setProps({"columnResized": column._column.field})
//         },
//         // based on http://tabulator.info/docs/4.8/column-calcs#func-custom
//         ageCalc: function(values, data, calcParams){
//             //values - array of column values
//             //data - all table data
//             //calcParams - params passed from the column definition object
        
//             var calc = 0;
        
//             values.forEach(function(value){
//                 if(value > 18){
//                 calc ++;
//                 }
//             });
        
//             return calc;
//         }
//     }
// });