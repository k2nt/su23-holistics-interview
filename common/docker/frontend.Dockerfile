FROM node:16-alpine
WORKDIR /frontend
COPY /frontend/* .

RUN npm ci
RUN npm run build

CMD ["npm", "start"]