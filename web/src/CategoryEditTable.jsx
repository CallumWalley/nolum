import { ReactTabulator } from "react-tabulator";
import 'react-tabulator/lib/styles.css';
import "react-tabulator/lib/css/tabulator.min.css"
import { useEffect } from "react";

const columns=[
  {rowHandle:true, formatter:"handle", headerSort:false, frozen:true, width:30, minWidth:30},
  {title:"Name", field:"name", width:150},
  {title:"Progress", field:"progress", formatter:"progress", sorter:"number"},
  {title:"Gender", field:"gender"},
  {title:"Rating", field:"rating", formatter:"star", formatterParams:{stars:6}, hozAlign:"center", width:120},
  {title:"Favourite Color", field:"col"},
  {title:"Date Of Birth", field:"dob", hozAlign:"center", sorter:"date"},
  {title:"Driver", field:"car", hozAlign:"center", formatter:"tickCross"},
],

const data = [
    {id:1, date:"10/10/10", time:"1:00:00", amount:"100.50", from:"Example Person", thing:"Coffee", type:"Dropdown", category:"Category->Category", tags:"Tag tag tag", confidence:0.9, valid:true, input:"06-0169-0179253-04_Transactions_2019-02-16_2019-12-31.csv"},
  ];

function TransactionEditorTable() {
    useEffect(() => {
        
    })
    return (<ReactTabulator
        movableRows={true}
        data={data}
        columns={columns}
        tooltips={true}
        layout={"fitColumns"}
        />);
}

export default TransactionEditorTable;