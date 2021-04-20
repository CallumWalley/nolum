import './App.css';
import { useEffect, useState } from "react";
import TransactionEditorTable from "./TransactionEditorTable";
import { useBS, useInputSource } from "./models";

function CallumQuoteBox() {
  const {quote, error, isLoading } = useBS();
  if (quote === undefined) {
    return null;
  }
  return (<p id='daily-wisdom'>
    <i>{quote}</i>- Callum W.
  </p>);
}

// Yea, so this doesn't work. If I just send a serialised list, is that enough to generate it? xoxo
function InputFileList(){
  const { inputSource, isValidating, error } = useInputSource();
  return <ul>
    {inputSource.map(file => (
      <li key={file.filename}>{file.filename}</li>
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
              <div className="injest-file-header pseudo-dash">
                <p>Undigested input files</p>
                <button id='injest-file-selector-refresh-button' className="refresh-button">⟳</button>
              </div>
              <div className='radio-scroll' id='injest-file-selector-wrap'><InputFileList/></div>
            </div>
            <div className='file-select-table'>
              <div className="injest-file-header pseudo-dash">
                <p>Digested input files</p>
                <button className='refresh-button'>⟳</button></div>
              {/* <div className='radio-scroll'><InjestedFileList/></div> */}
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
