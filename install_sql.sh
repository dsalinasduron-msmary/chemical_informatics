sudo apt install python3-dev default-libmysqlclient-dev build-essential
pip install wheel
apt install pkg-config
export MYSQLCLIENT_CFLAGS=`pkg-config mysqlclient --cflags`
export MYSQLCLIENT_LDFLAGS=`pkg-config mysqlclient --libs`
pip install mysqlclient
