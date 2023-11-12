from flask import Flask, request

from utils import GeneralLimiter, PerClientLimiter

app = Flask(__name__)

limiter = GeneralLimiter()
default_limit: int = 5
update_every: int = 60


@app.route('/')
def get_limit():
    try:
        global limiter

        data = request.json
        ok = limiter(data.get('client', ''))
        return {'ok': ok}, 200 if ok else 429
    except Exception as e:
        print(e)
        return 'Internal server error', 500


@app.route('/params')
def change_params():
    try:
        global limiter
        global default_limit
        global update_every

        data = request.json
        default_limit = data.get('default_limit', default_limit)
        update_every = data.get('update_every', update_every)

        if not isinstance(limiter, eval(data.get('limiter', limiter.__class__.__name__))):
            limiter = eval(data.get('limiter', limiter.__class__.__name__))(default_limit, update_every)
        return '', 200
    except Exception as e:
        print(e)
        return 'Internal server error', 500


@app.route('/register')
def register_client():
    try:
        global limiter
        global default_limit

        data = request.json
        if 'client' not in data:
            return 'Client name is absent', 403
        if isinstance(limiter, PerClientLimiter):
            limiter.register_client(client=data.get('client'), limit=data.get('limit', default_limit))
            print(f'Client {data.get("client")} registered. Limit is {data.get("limit", default_limit)}')
            return '', 200
        else:
            return 'Per client limiter is not available', 404
    except Exception as e:
        print(e)
        return 'Internal server error', 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)



