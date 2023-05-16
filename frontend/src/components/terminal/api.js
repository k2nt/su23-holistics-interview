import axios from 'axios'


const BACKEND_HOST = "localhost"
const BACKEND_PORT = 8000
const ROOT_BACKEND_URL = `http://${BACKEND_HOST}:${BACKEND_PORT}`


export async function createFile(path, forceCreate=false, data="") {
    return await axios.post(`${ROOT_BACKEND_URL}/cr`, {
        data: {
            path: path,
            forceCreate: forceCreate,
            data: data
        },
        config: {
            headers: {
                'Content-Type': 'application/json'
            }
        }
    })
}


export async function getFileContent(path) {
    return await axios.post(`${ROOT_BACKEND_URL}/cat`, {
        data: {
            path: path
        },
        config: {
            headers: {
                'Content-Type': 'application/json'
            }
        }
    })
}
