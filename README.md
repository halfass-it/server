# server

````
= READS
[ ] https://consteval.ca/2024/07/03/initialization/
[ ] https://concatenative.org/wiki/view/Modal
[ ] https://wryl.tech/projects/modal.html
[ ] https://www.youtube.com/watch?v=0PEFkDAokRI

````

````
=> TODO
[ ] fix fuzz with new updates; make it pass, router is hanging on gateway, it should forward to auth and game, then push answer back to client

[ ] mypy type checking - https://mypy.readthedocs.io/en/stable/

[ ] auth server with google auth

[ ] auth db
Backup for PostgreSQL:
For backing up your PostgreSQL database, you can use the built-in pg_dump utility or a tool like pg_backup. Here's an example of using pg_dump to create a backup:
pg_dump -U postgres -d mydatabase > backup.sql
You can automate this process using cron jobs or a backup management tool like PostgreSQL Backup and Restore (pbr).
/auth_server
/gameplay_server
````

````
=> Requirements
> python>=3.11
> python-venv
> nginx
````
