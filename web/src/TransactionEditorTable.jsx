import { ReactTabulator } from "react-tabulator";
import 'react-tabulator/lib/styles.css';
import "react-tabulator/lib/css/tabulator.min.css"
import { useEffect } from "react";

const columns = [
    { title: "Date", field: "date", sorter: "date"},
    { title: "Time", field: "time", sorter: "time"},
    { title: "Amount", field: "amount", sorter:"numeric", formatter:"money",},
    { title: "From", field: "from"},
    { title: "Item/Service", field: "thing", editor:"input"},
    { title: "Payment Type", field: "type" },
    { title: "Category", field: "category", headerSort: false},
    { title: "Tags", field: "tags", headerSort: false},
    { title: "Confidence", field: "confidence", sorter:"numeric", formatter: "progress", formatterParams:{min:0, max:1,legendColor:"#FFFFFF", legend:function(value){return `${value*100}%`}}},
    { title: "Input File", field: "input", sorter: "string"},
    { title: "", field: "valid", formatter: "tickCross", editor: "tickCross", headerSort: false, width:2}
  ];

const data = [
    {id:1, date:"10/10/10", time:"1:00:00", amount:"100.50", from:"Example Person", thing:"Coffee", type:"Dropdown", category:"Category->Category", tags:"Tag tag tag", confidence:0.9, valid:true, input:"06-0169-0179253-04_Transactions_2019-02-16_2019-12-31.csv"},
  ];

function TransactionEditorTable() {
    useEffect(() => {
        
    })
    return (<ReactTabulator
        data={data}
        columns={columns}
        tooltips={true}
        layout={"fitColumns"}
        />);
}

export default TransactionEditorTable;