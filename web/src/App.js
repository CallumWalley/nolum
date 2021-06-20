import './App.css';
import { useEffect, useState } from "react";
import TransactionEditorTable from "./TransactionEditorTable";
import { useBS, useInputSource, useInjestedSource, useInjestData } from "./models";

function CallumQuoteBox() {
  const { quote, error, isLoading } = useBS();
  if (quote === undefined) {
    return null;
  }
  return (<p id='daily-wisdom'>
    <i>{quote}</i>- Callum W.
  </p>);
}

function InputFileList() {
  const { inputSource, isValidating, error } = useInputSource();
  const sayFuck = () => alert('FUCK');
  const data = new FormData(form.current);
  const inputPost = () => {
    fetch('http://localhost:5000/input-files', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        data
      })
    })
  }


  if (!inputSource) return <ul></ul>
//  return  <form action="http://localhost:5000/input-files" method="post">
return  <form onChange={inputPost} method="post">
    {inputSource.map((file, index) => (
      <li className="pseudo-tabulate-row" key={index + file.filename}><input type="checkbox"></input>{file.filename}</li>
    ))}
  </form>;
}

//TODO Make whole row active element, not just checkbox.
function InjestedFileList() {
  const { inputSource, isValidating, error } = useInjestedSource();
  if (!inputSource) return <ul></ul>
  return <ul>
    {inputSource.map((file, index) => (
      <li className="pseudo-tabulate-row" key={index + file.filename}><input type="button" ></input>{file.filename}</li>
    ))}
  </ul>;
}
// function InjestedFileList(){
//   return
// }
// InputFileOnChange = () => {
//   this.setState(initialState => ({
//     isApple: !initialState.isAvocado,
//   }));
// }

// class InjestedFileList extends React.Component {

//   constructor(props) {
//     super(props);
//     this.state = {value: 'coconut'};

//     this.handleChange = this.handleChange.bind(this);
//     this.handleSubmit = this.handleSubmit.bind(this);
//   }

//   handleChange(event) {
//     this.setState({value: event.target.value});
//   }

//   handleSubmit(event) {
//     alert('Your favorite flavor is: ' + this.state.value);
//     event.preventDefault();
//   }

//   readFS(event) {
//     const { inputSource, isValidating, error } = useInjestedSource();
//   }

//   render() {    
//     if (!inputSource) return <ul></ul>
//     return <form onSubmit={this.handleSubmit}>
//       {inputSource.map((file, index) => (
//         <li className="pseudo-tabulate-row" key={index + file.filename}><input type="button" ></input>{file.filename}</li>
//       ))}
//     </form>
//   }
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
              <div className='radio-scroll pseudo-tabulate' id='injest-file-selector-wrap'><InputFileList /></div>
              <div>
                {/* <form action="http://localhost:5000/input-files" method="post">
                  <p>Testpost:</p>
                  <p><input type="text" name="list" /></p>
                  <p><input type="submit" value="submit" /></p>
                </form> */}
              </div>
            </div>
            <div className='file-select-table'>
              <div className="injest-file-header">
                <p>Digested input files</p>
                <button className='refresh-button'>⟳</button></div>
              <div className='radio-scroll pseudo-tabulate'><InjestedFileList /></div>
            </div>
          </div>
        </div>
        <div id='injestion-team' className='team'>
          <h3>Injest Tagged Data</h3>
          <TransactionEditorTable />
          <input type="submit" name="injest" formaction="http://localhost:5000/injest-data" method="POST" value="injest-data"></input>
        </div>
      </div>
      <div id='metrics' className='department'><h2>Metrics</h2>
      </div>
    </div>
  );
};
export default App;
