# Use official PostgreSQL image as base
FROM postgres:latest

# Enable password authentication
RUN echo "host all all 0.0.0.0/0 md5" >> /var/lib/postgresql/data/pg_hba.conf

# Set password for 'postgres' user
RUN echo "ALTER USER postgres WITH PASSWORD 'admin';" | docker-entrypoint.sh postgres

