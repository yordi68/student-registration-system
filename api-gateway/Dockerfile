# Use the official Nginx image from Docker Hub
FROM nginx:latest

# Set environment variable for Consul host
ENV CONSUL_HOST=consul

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80
