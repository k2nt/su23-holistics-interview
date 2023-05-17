import { useState } from 'react';
import './terminal.css';
import parseCommand from './cli-parser';
import { createFile, findFile, getFileContent, listSubFiles, moveFile, removeFile, updateFile } from './api';
import { HttpStatusCode } from 'axios';



export const Terminal = () => {
    const [terminalHistories, setTerminalHistories] = useState([])
    const [workDir, setWorkDir] = useState("~")


    return(
        <div className="terminal">
            <TerminalHistories />
            <TerminalPrompt />
        </div>
    );


    function TerminalHistory(data, idx) {
        return(
            <div className="terminal__prompt" key={idx}>
                <div className="terminal__prompt__command">
                    <div className="terminal__prompt__label">{workDir}</div>
                    <div className="terminal__prompt__input">
                        <input
                            type="text"
                            key="command"
                            value={data.command}
                            disabled={true}
                        />
                    </div>
                </div>
                <Response response={data.response}/>
            </div>
        )


        function Response(response) {
            response = response.response
            
            if (response === null) {
                return(<></>)
            }

            if (response.constructor === Array) {
                response = response.map((x, id) => <li key={id}>{JSON.stringify(x)}</li>)
                return(
                    <div className="terminal__prompt__response">
                        <ul>{response}</ul>
                    </div>
                )
            } else if (response.constructor === Object) {
                response = JSON.stringify(response)
                return(
                    <div className="terminal__prompt__response">
                        {response}
                    </div>
                )
            }

            return(
                <div className="terminal__prompt__response">
                    {response}
                </div>
            )
        }
    }


    function TerminalPrompt() {
        return(
            <div className="terminal__prompt__command" key="latest">
                <div className="terminal__prompt__label">{workDir}</div>
                <div className="terminal__prompt__input">
                    <input
                        type="text"
                        onKeyDown={handleKeyDown}
                        autoFocus
                    />
                </div>
            </div>
        )


        async function handleKeyDown(event) {
            if (event.key !== "Enter")
                return;
            
            let command = event.target.value
            let commandParsed = []
            let response = ""

            try {
                commandParsed = parseCommand(command)
            } catch (e) {
                response = command === '' ? '' : e.message
            } 

            console.log("commandParsed", commandParsed)
            
            if (response === "") {
                const apiHandler = {
                    cr: {
                        fn: createFile,
                        method: "POST"
                    },
                    ls: {
                        fn: listSubFiles,
                        method: "GET"
                    },
                    cat: {
                        fn: getFileContent,
                        method: "GET"
                    },
                    mv: {
                        fn: moveFile,
                        method: "POST"
                    },
                    rm: {
                        fn: removeFile,
                        method: "DELETE"
                    }, 
                    find: {
                        fn: findFile,
                        method: "GET"
                    },
                    up: {
                        fn: updateFile,
                        method: "UPDATE"
                    }
                }

                const cmd = commandParsed.cmd
                if (apiHandler[cmd] !== undefined) {
                    const promise = apiHandler[cmd].fn(commandParsed)
                    response = await promise
                        .then(resp => {
                            if (resp.status < 200 || resp.status > 299) {
                                return `error: HTTP ${resp.status}`
                            } else {
                                return apiHandler[cmd].method === "GET" ? resp.data['data'] : ""
                            }
                        }).catch(error => {
                            console.log(error)
                            return `error: ${error.message}`
                        })
                }
            }


            console.log("response", response.constructor === Array)

            const newHistory = {
                path: workDir,
                command: command,
                response: response,
                idx: terminalHistories.length
            }
            setTerminalHistories([...terminalHistories, newHistory])     
        }
    }


    function TerminalHistories() {
        return(
            terminalHistories.map(
                (data, idx) => TerminalHistory(data, idx)
            )
        )
    }
};
