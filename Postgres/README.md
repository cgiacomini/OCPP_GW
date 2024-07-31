## Install PostgreSQL

```
$ sudo apt update
$ sudo apt install postgresql postgresql-contrib
```

## Verifiy the installation
```
sudo -u postgres psql -c "SELECT version();"
----------------------------------------------------------------------------------------------------------------------------------------
 PostgreSQL 14.12 (Ubuntu 14.12-0ubuntu0.22.04.1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0, 64-bit
(1 row)
```

## Postgres Setup

1. Allow connection with no password from localhost.
Add this line in ***/etc/postgresql/14/main/pg_hba.conf*** to allow connection to the database with no password
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             127.0.0.1/32            trust
```

2. Give a password to the 'postgres' default admin user
Add this line in ***/etc/postgresql/14/main/pg_hba.conf*** to allow connection to the database with password
```
## Allow local connections with password
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
```

In both case restart the service
```
$ sudo service postgresql restart
$ sudo service postgresql status
● postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (/lib/systemd/system/postgresql.service; enabled; vendor preset: enabled)
     Active: active (exited) since Wed 2024-07-03 15:55:17 CEST; 33min ago
    Process: 92468 ExecStart=/bin/true (code=exited, status=0/SUCCESS)
   Main PID: 92468 (code=exited, status=0/SUCCESS)

Jul 03 15:55:17 DESKTOP-RMKPUK6 systemd[1]: Starting PostgreSQL RDBMS...
Jul 03 15:55:17 DESKTOP-RMKPUK6 systemd[1]: Finished PostgreSQL RDBMS.
```

3. Give "postgres" default admin use a password
```
$ sudo su - postgres
$ psql
ALTER USER postgres WITH PASSWORD 'admin';
\q
```

## Connect to the database

```
$  psql -U postgres -h 127.0.0.1 -W -d postgres
Password:
psql (14.12 (Ubuntu 14.12-0ubuntu0.22.04.1))
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
Type "help" for help.

# list all databases
postgres=# \l
 postgres  | postgres | UTF8     | C.UTF-8 | C.UTF-8 | 
 template0 | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres          +
           |          |          |         |         | postgres=CTc/postgres
 template1 | postgres | UTF8     | C.UTF-8 | C.UTF-8 | =c/postgres          +
           |          |          |         |         | postgres=CTc/postgres

# list roles
postgres=# \du
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
 singleton |                                                            | {}
 
```
## Create user and database
```
$ cd Databases
$ python create_database.py  --config ../config.cfg  --sql create_database.sql 
Executed: --- Clean up
DROP TABLE IF EXISTS charging_stations
Executed: DROP DATABASE IF EXISTS "singleton-ev"
Executed: DROP USER IF EXISTS singleton
Executed: -- Drop user if exists


-- Create database
CREATE DATABASE "singleton-ev"
Executed: -- Create user
CREATE USER singleton WITH PASSWORD 'singleton123'
Executed: -- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE "singleton-ev" TO singleton
Executed: -- Create table
CREATE TABLE IF NOT EXISTS charging_stations (
    id SERIAL PRIMARY KEY,
    serial_number VARCHAR(25),
    iccid VARCHAR(20),
    imsi VARCHAR(20),
    firmware_version VARCHAR(50),
    charge_box_serial_number VARCHAR(255),
    charge_point_serial_number VARCHAR(255),
    meter_serial_number VARCHAR(255),
    meter_type VARCHAR(255),
    last_heartbeat TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    vendor_name VARCHAR(50) NOT NULL,
    model VARCHAR(20) NOT NULL,
    unique_id VARCHAR(255) UNIQUE NOT NULL
)
All SQL commands executed successfully
```
## Verification
First we try to connect with the newly created user
```
```