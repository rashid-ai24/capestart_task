# ============================================
# ClassHub Frontend Dockerfile
# Multi-stage build for React Application
# ============================================

# ============================================
# Stage 1: Base Node Image
# ============================================
FROM node:20-alpine as base

# Set work directory
WORKDIR /app

# Set environment variables
ENV NODE_ENV=development

# ============================================
# Stage 2: Development Image
# ============================================
FROM base as development

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci

# Copy project
COPY . .

# Expose port
EXPOSE 3000

# Default command
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# ============================================
# Stage 3: Build Dependencies
# ============================================
FROM base as build-deps

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci

# ============================================
# Stage 4: Production Build
# ============================================
FROM build-deps as build

# Copy project
COPY . .

# Build application
RUN npm run build

# ============================================
# Stage 5: Production Image with Nginx
# ============================================
FROM nginx:alpine as production

# Copy custom nginx config
COPY docker/nginx/frontend.conf /etc/nginx/conf.d/default.conf

# Copy built application
COPY --from=build /app/dist /usr/share/nginx/html

# Create necessary directories
RUN mkdir -p /usr/share/nginx/html

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
