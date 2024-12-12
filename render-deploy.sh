set -e
if [ ! -d "migrations" ]; then

    flask --app src.app db init
fi
flask --app src.app db migrate -m "Automated migration"
# Atualizar o banco de dados
flask --app src.app db upgrade

# Iniciar o servidor com Gunicorn
gunicorn src.wsgi:app --bind 0.0.0.0:5000