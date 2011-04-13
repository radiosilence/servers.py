for i in $(ls /etc/init.d | grep gunicorn_); do
	service $i stop
	service $i start
done
