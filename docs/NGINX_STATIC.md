**Nginx static serving (example)**

Example Nginx configuration to serve Django static files from `STATIC_ROOT` (e.g. `/var/www/project/staticfiles`).

Adjust `alias` to your deployed `STATIC_ROOT` path.

server {
  listen 80;
  server_name example.com;

  location /static/ {
    alias /var/www/project/staticfiles/;
    access_log off;
    expires 30d;
    add_header Cache-Control "public, max-age=2592000";
  }

  location / {
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_pass http://unix:/run/gunicorn.sock; # or http://127.0.0.1:8000
  }
}

Notes:
- Use `alias` (not `root`) so `/static/whatever` maps to `/var/www/project/staticfiles/whatever`.
- Set proper file permissions so Nginx can read the static files.
- Consider adding `gzip_static on;` if you pre-compress assets.
