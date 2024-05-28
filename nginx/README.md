# NGINX as a Docker Container

### Create Environment

```bash
touch .env
```

- Add any properties if required

## Create a local host 

**NOTE : Ignore if you have public domain poit it to server IP where you run nginx**

```bash
sudo echo "127.0.0.1 test.nginx.com" >> /etc/hosts
```

## Clone

```bash
    git clone https://github.com/JinnaBalu/docker-nginx-ssl.git
```

## Edit based on yur change

*nginx.conf*

1. Change the below property where you want to redirect to

```txt
proxy_pass https://github.com/JinnaBalu;
```

If you are able to access your app from http://123.12.1.4:8080/, then this property looks something like this

```txt
proxy_pass http://123.12.1.4:8080/;
```

2. Copy your ssl files and Rename the .crt, .key files based on your file names

```txt
Either rename nginx.key , nginx.crt files in ssl folder 

OR

in *nginx.conf* rename the value of the properties ssl_certificate, ssl_certificate_key
```

3. Change log files location on your host OS
```txt
Change "~/docker-nginx-app-logs" and "~/docker-nginx-proxy-logs/" in "docker-nginx/docker-compose.yml"
```

```bash
docker-compose up -d
```

If you find any issues please raise and issue on issues tab


## USE CASES

- Proxy 
- Zero downtime with load balancer
- Pen Configurations for security
- SEO management 
- Static content between servers
- Maintanance page
- Configure the Local hosts with the local domains `/etc/hosts`
- configure letsencrypt
- configure self signed certificate