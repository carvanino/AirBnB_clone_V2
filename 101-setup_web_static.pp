#Sets up your web servers for the deployment of web_static using Puppet

exec {'Installs Nginx':
path    => '/usr/bin',
command => 'sudo apt-get -y install nginx',
}

file {'/data/web_static/releases/test/index.html':
ensure  => 'present',
content => 'Fake Content',
}

exec {'Make directories':
path    => '/usr/bin',
command => 'mkdir -p /data/web_static/releases/'
}

file {'/data/web_static/current':
ensure => 'link',
target => '/data/web_static/releases/test'
}

exec {'Change user && group':
path    => '/usr/bin',
command => "sudo chown -R 'ubuntu:ubuntu' /data/",
}

file {'/var/www/html/error404.html':
ensure  => present,
content => "Ceci n'est pas une page"
}

exec {'block server':
path    => '/usr/bin',
command => 'echo "
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;

        add_header X-Served-By \$HOSTNAME;

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
}" | sudo tee /etc/nginx/sites-available/default'
}


exec {'Restart Nginx':
path    => '/usr/bin',
command => 'sudo service nginx restart',
}
