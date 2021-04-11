import { useEffect, useState } from "react";

function InputSourceList({id}) {
    const [inputList, setInputList] = useState(undefined);
    useEffect(() => {
        fetch("/input-files/").then(response => {
            if (!response.ok) {
                throw new Error(response.statusText)
            }
            return response.json();
        }).then(inputList => {
            setInputList(inputList);
        })
    }, [])
    return (<)
}