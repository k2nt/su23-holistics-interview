import { useState } from 'react';
import './terminal.css';


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
                                    value={data.response}
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

            const newHistory = {
                path: workDir,
                command: event.target.value,
                response: event.target.value,
                idx: terminalHistories.length
            }

            setTerminalHistories([...terminalHistories, newHistory])
            event.target.value = ""
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