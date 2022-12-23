#!/usr/bin/env bash
# Sets up web serves for deployment of web static

sudo apt-get -y install nginx
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
echo "
<html>
	<head>
	</head>
	<body>
		Fake content
	</body>
</html>
" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R "ubuntu:ubuntu" /data/
echo "
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;

        add_header X-Served-By $HOSTNAME;

        error_page 404 /error404.html;
        location = /error404.html {
                root /var/www/html;
                internal;
        }

        location /redirect_me {
                return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
        }
	location /hbnb_static {
		alias /data/web_static/current/;
		index index.html index.htm;
	}
}" | sudo tee /etc/nginx/sites-available/default
# sed -i '12i location /data/web_static/current/ { alias /hbnb_static/; }' /etc/nginx/sites-available/default

sudo service nginx restart
