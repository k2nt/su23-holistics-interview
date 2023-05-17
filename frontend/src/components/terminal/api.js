import axios from 'axios'


const BACKEND_HOST = "localhost"
const BACKEND_PORT = 8000
const ROOT_BACKEND_URL = `http://${BACKEND_HOST}:${BACKEND_PORT}`
const FS_URL_PREFIX = "fs"



export async function createFile({path, forceCreate=false, data=""}) {
    console.log(path)
    return await axios.post(`${ROOT_BACKEND_URL}/${FS_URL_PREFIX}/cr`, {
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
    return await axios.post(`${ROOT_BACKEND_URL}/${FS_URL_PREFIX}/cat`, {
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


export async function listSubFiles({path}) {
}



export async function moveFile({source, dest}) {

}


export async function removeFile({path}) {

}


export async function findFile({name, folderPath}) {

}


export async function updateFile({path, name, data=""}) {

}


export async function changeWorkDirectory(path) {

}
