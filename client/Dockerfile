# Use the official Node.js runtime image as the base image
FROM node:14

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application's files
COPY . .

# Build the application
RUN npm run build

# Expose the port on which the application will be served
EXPOSE 4200

# Start the application
CMD ["npm", "start"]