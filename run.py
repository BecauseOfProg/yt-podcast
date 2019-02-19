from app import app
from views import index, channel, download


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
