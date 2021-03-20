import './App.css';
import { useEffect, useState } from "react";

function CallumQuoteBox() {
  const [quote, setQuote] = useState();
  useEffect(() => {
    // Fetch the freshest bull.
    fetch("/bullshit").then(
      response => {
        if (!response.ok){
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
  return (<p>
    {quote} - Callum W.
  </p>)
}



function App() {
  return (
    <div className="App">
      <h1>NoLum Cloud-Native Deep-Learning Hyper-Ledger, v2</h1>
      <CallumQuoteBox />
      <h2>Ingest new data</h2>

    </div>
  );
}

export default App;
