# production stage
FROM nginx:latest as production-stage
COPY nginx/nginx-conf.conf /etc/nginx/nginx.conf
COPY backend/static /usr/src/app/static/
COPY backend/media /usr/src/app/media/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]