FROM node:20-slim

WORKDIR /app

# Copy lockfiles and install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy source code
COPY . .

EXPOSE 5173

# Expose host flag so Vite can accept requests from outside the container
CMD ["npm", "run", "dev", "--", "--host"]
