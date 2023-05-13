FROM node:16.17-alpine
# Create app directory
WORKDIR /frontend

# Install dependencies
RUN apk update && \
    apk add git
COPY package*.json yarn.lock ./
RUN yarn install --frozen-lockfile
COPY . .
RUN yarn build

# Start application
CMD ["yarn", "start"]
