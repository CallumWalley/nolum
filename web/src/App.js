import './App.css';
import { useEffect, useState } from "react";
import TransactionEditorTable from "./TransactionEditorTable";
import { useBS, useInputSource, useInjestedSource } from "./models";

function CallumQuoteBox() {
  const {quote, error, isLoading } = useBS();
  if (quote === undefined) {
    return null;
  }
  return (<p id='daily-wisdom'>
    <i>{quote}</i>- Callum W.
  </p>);
}

function InputFileList(){
  const { inputSource, isValidating, error } = useInputSource();
  if (! inputSource) <ul></ul>
  return <ul>
    {inputSource.map((file, index) => (
      <li className="pseudo-tabulate-row" key={index + file.filename}><input type="checkbox"></input>{file.filename}</li>
    ))}
  </ul>;
}

function InjestedFileList(){
  const { inputSource, isValidating, error } = useInjestedSource();
  if (! inputSource) return <ul></ul>
  return <ul>
    {inputSource.map((file, index) => (
      <li className="pseudo-tabulate-row" key={index + file.filename}><input type="button"></input>{file.filename}</li>
    ))}
  </ul>;
}
// function InjestedFileList(){
//   return
// }

function App() {
  return (
    <div className="App">
      <h1>NoLum<sup>&copy;</sup> Cloud-Native Deep-Learning Hyper-Ledger  <small>v2.0.0</small></h1>
      <CallumQuoteBox />
      <div id="operations-department" className="department">
        <h2>Operations</h2>
        <div id="acquisitions-team" className="team">
          <h3>Acquire new Data</h3>
          {/* <label>Target Account</label> */}
          <div id="file-select-tables">
            <div className="file-select-table">
              <div className="injest-file-header">
                <p>Undigested input files</p>
                <button id='injest-file-selector-refresh-button' className="refresh-button">⟳</button>
              </div>
              <div className='radio-scroll pseudo-tabulate' id='injest-file-selector-wrap'><InputFileList/></div>
            </div>
            <div className='file-select-table'>
              <div className="injest-file-header">
                <p>Digested input files</p>
                <button className='refresh-button'>⟳</button></div>
              <div className='radio-scroll pseudo-tabulate'><InjestedFileList/></div>
            </div>
          </div>
      </div>
      <div id='injestion-team' className='team'>
        <h3>Injest Tagged Data</h3>
        <TransactionEditorTable />
          <button>Injest</button>
        </div>
      </div>
      <div id='metrics' className='department'><h2>Metrics</h2>
</div>
    </div>
  );
};
export default App;
