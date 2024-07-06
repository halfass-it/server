# server

````
= READS
[ ] https://consteval.ca/2024/07/03/initialization/

````

````
=> TODO
[ ] fix fuzz with new updates; make it pass

[ ] update docs 

[ ] memcache utils

[ ] mypy type checking - https://mypy.readthedocs.io/en/stable/

[ ] auth server with google auth

[ ] auth db
Backup for PostgreSQL:
For backing up your PostgreSQL database, you can use the built-in pg_dump utility or a tool like pg_backup. Here's an example of using pg_dump to create a backup:
pg_dump -U postgres -d mydatabase > backup.sql
You can automate this process using cron jobs or a backup management tool like PostgreSQL Backup and Restore (pbr).
/auth_server
/gameplay_server

[ ] cdn
Content Delivery Network (CDN):
For serving static assets through a CDN, you can use a CDN service provider like Cloudflare, Amazon CloudFront, or Fastly. These services allow you to cache and distribute your static content globally for better performance and reduced latency.
Alternatively, you can self-host a CDN using a tool like Nginx, Apache Traffic Server, or Varnish Cache.
Here's an example of configuring NGINX to serve static assets:
server {
    listen 80;
    server_name example.com;

    location /static/ {
        root /path/to/static/files;
        expires 30d;
    }

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
    }
}
/router


````


````
=> Requirements
> python>=3.11
> python-venv
> nginx
````
