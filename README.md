Current dependencies:
- postgresql-9.4
- python3-psycopg2
- sqlalchemy

Notes:
1) "createuser -P -s -e admin" from postgres user;
   "alter role with replication" from psql-command-line;

2) for remote access:
     edit /etc/postgresql/9.4/main/postgresql.conf (set listen_addresses = '*' for all ip's)
     edit /etc/postgresql/9.4/main/pg_hba.conf
