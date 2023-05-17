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
                {
                    data.response !== "" ?
                        <div className="terminal__prompt__response">
                            <div className="terminal__prompt__input">
                                <input
                                    type="text"
                                    key="command"
                                    value={data.response.toString()}
                                    disabled={true}
                                />
                            </div>
                        </div>
                    : 
                        <></>
                }
            </div>
        )
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
                    cr: createFile,
                    ls: listSubFiles,
                    cat: getFileContent,
                    mv: moveFile,
                    rm: removeFile,
                    find: findFile,
                    up: updateFile,
                }

                if (apiHandler[commandParsed.cmd] !== undefined) {
                    const promise = apiHandler[commandParsed.cmd](commandParsed)
                    response = await promise
                        .then(resp => {
                            if (resp.status !== HttpStatusCode.Created) {
                                return `error: HTTP ${resp.status}`
                            } else {
                                return resp.data
                            }
                        }).catch(error => {
                            console.log(error)
                            return `error: ${error.message}`
                        })
                }
            }
            
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
