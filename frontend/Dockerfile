FROM node:19-alpine

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./
RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent

# ENV PATH /app/node_modules/.bin:$PATH

COPY src ./src
COPY public ./public
RUN npm run build