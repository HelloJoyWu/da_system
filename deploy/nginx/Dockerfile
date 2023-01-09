FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx.system.conf /etc/nginx/sites-available/
COPY uwsgi_params /etc/nginx/uwsgi_params

RUN mkdir -p /etc/nginx/sites-enabled/ \
    && ln -s /etc/nginx/sites-available/nginx.system.conf /etc/nginx/sites-enabled/ \
    && rm /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]
