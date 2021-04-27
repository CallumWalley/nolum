import { ReactTabulator } from "react-tabulator";
import 'react-tabulator/lib/styles.css';
import "react-tabulator/lib/css/tabulator.min.css"
import { useEffect } from "react";
import { render } from "react";
import { moment } from "moment"


// //Create Date Editor
// var dateEditor = function(cell, onRendered, success, cancel){
//     //cell - the cell component for the editable cell
//     //onRendered - function to call when the editor has been rendered
//     //success - function to call to pass the successfuly updated value to Tabulator
//     //cancel - function to call to abort the edit and return to a normal cell
//     return
//     // delete this obv

//     //create and style input
//     var cellValue = moment(cell.getValue(), "DD/MM/YYYY").format("YYYY-MM-DD"),
//     input = document.createElement("input");

//     input.setAttribute("type", "date");

//     input.style.padding = "4px";
//     input.style.width = "100%";
//     input.style.boxSizing = "border-box";

//     input.value = cellValue;

//     onRendered(function(){
//         input.focus();
//         input.style.height = "100%";
//     });

//     function onChange(){
//         if(input.value != cellValue){
//             success(moment(input.value, "YYYY-MM-DD").format("DD/MM/YYYY"));
//         }else{
//             cancel();
//         }
//     }

//     //submit new value on blur or change
//     input.addEventListener("change", onChange);
//     input.addEventListener("blur", onChange);

//     //submit new value on enter
//     input.addEventListener("keydown", function(e){
//         if(e.keyCode == 13){
//             onChange();
//         }

//         if(e.keyCode == 27){
//             cancel();
//         }
//     });

//     return input;
// };

// This adds the dropdown 'raw string' thingie. Might need to be 'reactified'

// function rowFormatter(row){
//     //create and style holder elements
//     row.getElement().appendChild(render(<div className="rawStringPanelParent"><div className="rawStringPanel"><p>{row.getData().rawString}</p></div></div>));
// }

// var rawStringRowFormatter = function(row, formatterParams){
//   //cell - the cell component
//   //formatterParams - parameters set for the column
//   row.getElement().innerHTML+=`<div id={row.get}>${row.getData.rawString}</div>`
//   //return `<button>click</button><div class="test-class-child">${cell.getValue()}</div>` //return the contents of the cell;
// }

const columns = [
    { title: "Date", field: "date", sorter:"date"}, // editor:dateEditor},
    { title: "Time", field: "time", sorter: "time"},
    { title: "Amount", field: "amount", sorter:"numeric", formatter:"money",},
    { title: "From", field: "from"},
    { title: "Item/Service", field: "thing", editor:"input"},
    { title: "Payment Type", field: "type" },
    { title: "Category", field: "category", headerSort: false},
    { title: "Tags", field: "tags", headerSort: false},
    { title: "Confidence", field: "confidence", sorter:"numeric", formatter: "progress", formatterParams:{min:0, max:1,legendColor:"#FFFFFF", legend:function(value){return `${value*100}%`}}},
    { title: "Input File", field: "input", sorter: "string"},
    { title: "", field: "valid", formatter: "tickCross", editor: "tickCross", headerSort: false, width:2},
    { title: "", field: "rawString"},
  ];

const data = [
    {id:1, date:"10/10/10", time:"1:00:00", amount:"100.50", from:"Example Person", thing:"Coffee", type:"Dropdown", category:"Category->Category", tags:"Tag tag tag", confidence:0.9, valid:true, input:"06-0169-0179253-04_Transactions_2019-02-16_2019-12-31.csv", rawString:"Visa Purchase,4835-****-****-2031  Df,      0.71,Google  Clou,        0.04,-3.53,04/02/2021,USD 2.48 converted at 0.71,This includes a currency conversion charge of $0.04"},
    {id:2, date:"10/10/10", time:"1:00:00", amount:"100.50", from:"Example Person", thing:"Coffee", type:"Dropdown", category:"Category->Category", tags:"Tag tag tag", confidence:0.2, valid:false, input:"06-0169-0179253-04_Transactions_2019-02-16_2019-12-31.csv", rawString:"Visa Purchase,4835-****-****-2031  Df,      0.71,Google  Clou,        0.04,-3.53,04/02/2021,USD 2.48 converted at 0.71,This includes a currency conversion charge of $0.04"},
  ]
  ;

function TransactionEditorTable() {
    useEffect(() => {
        
    })
    return (<ReactTabulator
        data={data}
        columns={columns}
        tooltips={true}
        layout={"fitColumns"}
        dataTree={true}
        dataTreeCollapseElement={"<i class='fas fa-minus-square'></i>"}
        //rowFormatter={rawStringRowFormatter}
        
        />);
}

export default TransactionEditorTable;