import './App.css';
import { useEffect, useState } from "react";
import TransactionEditorTable from "./TransactionEditorTable";

function CallumQuoteBox() {
  const [quote, setQuote] = useState();
  useEffect(() => {
    // Fetch the freshest bull.
    fetch("/bullshit").then(
      response => {
        if (!response.ok) {
          throw new Error(response.statusText);
        }
        return response.text();
      }
    ).then(content => {
      setQuote(content);
    }).catch(error => {
      console.error("Error occurred while fetching Callum's quotes", error);
      setQuote(":(")
    });
  }, [setQuote]);
  if (quote === undefined) {
    return null;
  }
  return (<p id='daily-wisdom'>
    {quote} - Callum W.
  </p>)
}

function InputFileList(){
  return
}

function InjestedFileList(){
  return
}

function App() {
  return (
    <div className="App">
      <h1>NoLum Cloud-Native Deep-Learning Hyper-Ledger, v2</h1>
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
              <div className='radio-scroll'><InjestedFileList/></div>
            </div>
          </div>
      </div>
      <div id='injestion-team' className='team'>
        <h3>Injest Tagged Data</h3>
          <button>Injest</button>
        </div>
      </div>
      <div id='metrics' className='department'><h2>Metrics</h2>
</div>
    </div>
  );
};
export default App;
