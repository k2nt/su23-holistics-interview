import { useState } from 'react';
import './terminal.css';
import parseCommand from './cli-parser';
import { createFile, getFileContent } from './api';



export const Terminal = () => {
    const [terminalHistories, setTerminalHistories] = useState([])
    const [workDir, setWorkDir] = useState("Documents")


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


        function handleKeyDown(event) {
            if (event.key !== "Enter")
                return;
            
            let command = event.target.value
            let commandParsed = []
            let response = ""

            try {
                commandParsed = parseCommand(command)
                response = commandParsed
            } catch (e) {
                response = e.message
            } 

            // Debug
            // DELETE ME
            console.log("command", commandParsed.cmd)
            console.log("response", response)

            let promise = ""
            switch (commandParsed.cmd) {
                case "cr":
                    promise = createFile(commandParsed.path, commandParsed.forceCreate, commandParsed.data)
                    promise
                        .then(resp => {
                            console.log(resp)
                        }).catch(e => {
                            console.log(e)
                        })
                    break

                case "cat":
                    promise = getFileContent(parseCommand.path)
                    break
                case "ls":
                    break;
                case "mv":
                    break;
                case "rm":
                    break;
                case "find":
                    break;
                case "up":
                    break;
                default:
                    break;
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
