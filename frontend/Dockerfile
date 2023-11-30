FROM node:19-alpine

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./
RUN npm install --silent

# ENV PATH /app/node_modules/.bin:$PATH

COPY src ./src
COPY public ./public
RUN npm run build