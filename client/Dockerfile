FROM node:16-alpine

# set the working directory in the container
WORKDIR /usr/src/app

# copy the package.json and package-lock.json files
COPY package*.json ./

# install the dependencies
RUN npm install

# copy the rest of project files
COPY . .

RUN npm run build
EXPOSE 4200
CMD ["npm", "start"]