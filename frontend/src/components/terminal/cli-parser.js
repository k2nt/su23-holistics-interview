export default function parseCommand(command) {
    const tokens = command.split(" ")

    if (tokens.length === 0) 
        throw Error("error: empty command")

    switch (tokens[0]) {
        case "cr":
            if (tokens.length < 2)
                throw Error("usecase: cr [-p] PATH [DATA]")

            const force_create = tokens[1] === '-p'

            if (force_create && tokens.length === 2) 
                throw Error("error: cr [-p] PATH [DATA]")

            const path = force_create ? tokens[2] : tokens[1]
            
            let data = ""
            if (!force_create && tokens.length === 3)
                data = tokens[2]
            if (force_create && tokens.length === 4)
                data = tokens[3]

            return {"cmd": "cr", "path": path, "data": data}

        case "cat":
            if (tokens.length < 2)
                throw Error("usecase: cat FILE_PATH")
            return {"cmd": "cat", "path": tokens[1]}

        case "ls":
            if (tokens.length < 2)
                throw Error("usecase: ls FOLDER_PATH")
            return {"cmd": "ls", "path": tokens[1]}

        case "mv":
            if (tokens.length < 3)
                throw Error("usecase: mv PATH FOLDER_PATH")
            return {"cmd": "mv", "source": tokens[1], "dest": tokens[2]}

        case "rm":
            if (tokens.length < 4)
                throw Error("usecase: rm PATH [PATH2 PATH3...]")
            return {"cmd": "rm", "paths": tokens.slice(1)}

        case "find":
            if (tokens.length < 3)
                throw Error("usecase: find NAME FOLDER_PATH")
            return {"cmd": "find", "name": tokens[1], "folderPath": tokens[2]}
            
        case "up":
            if (tokens.length < 3)
                throw Error("usecase: up PATH NAME [DATA]")
            data = (tokens.length === 3) ? "" : tokens[3]
            return {"cmd": "up", "path": tokens[1], "name": tokens[2], "data": data}

        default:
            throw Error("error: unrecognized command")
    }
}
