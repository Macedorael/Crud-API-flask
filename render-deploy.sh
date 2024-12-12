set -e



flask run --app src.app db upgrade
flask run gunicorn src.wsgi:app
