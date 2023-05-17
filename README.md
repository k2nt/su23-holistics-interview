# Summer 2023 Holistics Interview Take-home Project Report

## Interviewee

Khai Nguyen -- tuankhai2k@gmail.com


## Overview

The goal of this project is to implement a file system in a relational database. The file system is provided as a web application. Users interact with the file system via a browser-based CLI, which sends requests to a backend service to manage the file system.

Due to time constraints, I was not able to fully implement the file system as requested. The current implementation contains a frontend and backend service that can be deployed locally. The three functioning CLI commands are `cr`, `ls`, and `cat` as listed in the requirements table.

## Getting Started

There are two ways to start the project. A Makefile has been 
prepared that contains all neccessary build tools.

### Prerequisites

For the backend, make sure Python is at least version 3.9.

For the frontend, make sure Node.js and Yarn is at the latest stable version.

Optionally, install Docker to run the application in a containerized environment.

### Deploy locally

To start the frontend service, change the work directory into the `frontend` folder and type `yarn start`

### Deploy via Docker

Change the working directory to the main project folder. From the CLI, type `make run` to launch the Docker containers and type `make run-build` to launch and rebuild.

There are two Docker containers that holds the frontend and backend service 
respectively. The frontend and backend application is exposed via port 3000 
and 8000 respectively and can be accessed via localhost.

## Design

### File System

 There are two types of files, data files and folders. Data file can hold data whereas folders are simply structures in which other folders can files can reside. Each file has a unique file ID (*fid*) as well as a unique absolute path name. The root folder is a special system folder that contains all other files and folders.

The file system is managed by 3 relational tables, which are *FileSystem*,
 *MetaData*, *Content*. The *FileSystem* table stores the tree structure of the file system through the parent relationship. Every folder, except for the root folder, in a file structure must have a single parent. The *MetaData* table stores metadata on files that includes the creation date, file size, pathname, and whether it is a folder or a data file. The *Content* table stores the file content for data files. Note that only files that are data files can appear in the *Contents* table.
 
 The three tables are designed to be 3NF (third normal form)-compliant to reduce data redundany. All three tables maintain a column hash-based index to optimize query performance. A hash-based index is chosen because we have mostly equal queries rather than range-based queries.

 The *FileSystem* table is considerd the "mother" table from which all other tables depend on via a foreign key relationship via the *fid* column.

 ### Tech stack

 The frontend is developed with React using Javascript. Packages are maintained and deployed using Yarn.

 The backend is implemented as a Flask application. Database interactions are managed by the Flask-SQLAlchemy engine through its ORM model.

 The frontend and backend communicates via HTTP requests and uses JSON as the message medium.

The database is SQLite for being relational, simple, and easy to setup.

 Docker is used to containerize and deploy the entire web application. Furthermore, I can deploy my Dockerized app on a cloud service like `fly.io` to publish my service.

 ## Architecture

The frontend is responsible for client CLI interactions. The CLI commands are passed through a lexer to be parsed and handed over to the backend to process.

The backend manages handles client requests and manages database interactions.

The database is not a separate service but rather embedded into the backend service. This is because I wanted to make develop the file system in time for submission.

## Future improvements

For this part, I will focus solely on how to improve the file system performace from a backend/database perspective. Due to time constraints on the project, I was not able to implement all the required functionalities in time. However, given more time, I would do the following to further improve the file system,

### Storing both forwards and backwards file structure relations

Currently, the *FileSystem* stores the parent folder of each file, where it keeps an index on the file ID column. While this is great of bottom-up operations like updating file sizes, it is not optimal for top-down operations like listing subdirectories. A solution is to make another table to store children relations. With these two tables, we can more efficiently perform both top-down and bottom-up operations.

### Concurreny

I can utilize concurreny to scale up my backend services. The backend service can manage a
threadpool to be able to handle multpiple requests at once and mitigate request queuing. Even more, with Docker and Kubernetes, I can have multiple instances of my backend running in true microservice scaling spirit.

### RPC

While HTTP requests are great for client-server connections, I can further optimize performance by using RPC has the communication medium between my services. RPC automates network connection and reduces overhead compared to traditional HTTP requests. Furthermore, RPC can make use of efficient binary-compressed formats like Protobuf compared to the less optimized JSON format.

### "Better" RDBMSes

I opted for SQLite for my implemenation due to its simplicity and low set-up efforts. However, SQLite lacks in performance compared to industry-standard choices like MySQL or PostgreSQL. An example of this would be in column indexing. SQLite only supports B-Tree index. While this is good-enough for my demo usecase, I would like to utilize better solutions like B+ Tree or Hash indexing offered by more complex RDBMSes.  
