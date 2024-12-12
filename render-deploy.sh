set -e

# Atualizar o banco de dados
flask --app src.app db upgrade

# Iniciar o servidor com Gunicorn
gunicorn src.wsgi:app --bind 0.0.0.0:5000