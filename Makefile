mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

msg:
	python3 manage.py makemessages -l uz -l en

compile_msg:
	python3 manage.py compilemessages -i .venv

loaddata:
	python3 manage.py loaddata categories brands faq features
