# Update connection string information obtained from the portal
""""
host = "posrgresql-prathap.postgres.database.azure.com"
user = "prathap@posrgresql-prathap"
dbname = "flaskmqtt_db"
password = "root@2021"
"""
SQLALCHEMY_DATABASE_URI = "postgresql://prathap@posrgresql-prathap:root@2021@posrgresql-prathap.postgres.database.azure.com/flaskmqtt_db"
#SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost/flaskmqtt_db"
SQLALCHEMY_TRACK_MODIFICATIONS = True