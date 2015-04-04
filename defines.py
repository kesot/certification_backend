USERS_PORT = 65010
SESSION_PORT = 65011
LOGIC_PORT = 65012
DB_PORT = 5432

DB_IP = "127.0.0.1"
MEMCACHED_IP = "127.0.0.1"

# one month (in seconds)
EXPIRATION_TIME = 2592000

CONNECTION_ADDRESS = 'postgresql+psycopg2://admin:admin@{0}:{1}/usersDB'.format(DB_IP, DB_PORT)

LOG_FORMAT = "%(levelname)-8s [LINE:%(lineno)d] %(filename)s %(message)s"
# must be changed
LOG_USERS_FNAME = "/home/yura/yurochko_fokin_certification_service/log/users.log"
LOG_SESSION_FNAME = "/home/yura/yurochko_fokin_certification_service/log/session.log"