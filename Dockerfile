# React-only Dockerfile
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install all dependencies (needed for building)
RUN npm install

# Copy React source files
COPY src/ ./src/
COPY public/ ./public/

# Build the React application
RUN npm run build

# Install serve to serve the built React app
RUN npm install -g serve

# Expose port 3000
EXPOSE 3000

# Start the React app on port 3000
CMD ["serve", "-s", "build", "-l", "3000"]