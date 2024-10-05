import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)


def get_user_by_id(con, _id):
    print("_id",_id)
    with con.cursor(dictionary=True) as cur:
        cur.execute('SELECT * FROM users WHERE id = %s', (_id,))
        return cur.fetchone()


@app.route('/api/users/<_id>', methods=['GET'])
def get_user(_id):
    with mysql.connector.connect(user='root', password='', host='localhost', database='sovelluskehykset_bad1') as con:
        with con.cursor() as cur:
            user = get_user_by_id(con, _id)
            return jsonify(user)


@app.route('/api/users/<_id>', methods=['DELETE'])
def delete_user(_id):
    with mysql.connector.connect(user='root', password='', host='localhost', database='sovelluskehykset_bad1') as con:
        with con.cursor() as cur:
            user = get_user_by_id(con, _id)
            if user is not None:
                cur.execute('DELETE FROM users WHERE id = (%s)', (_id,))
                con.commit()

                return "", 200
            return jsonify({'error': 'user not found'}), 404


@app.route('/api/users/<_id>', methods=['PUT'])
def edit_user(_id):
    req_data = request.get_json()
    with mysql.connector.connect(user='root', password='', host='localhost', database='sovelluskehykset_bad1') as con:
        with con.cursor() as cur:
            user = get_user_by_id(con, _id)
            if user  is not None:
                cur.execute('UPDATE users SET  username = %s, firstname = %s, lastname = %s WHERE id = %s',
                            (req_data['username'], req_data['firstname'], req_data['lastname'], user['id']))
                con.commit()
                req_data['id'] = user['id']
                return jsonify(req_data)

            return jsonify({'error': 'User not found'}), 404


@app.route('/api/users', methods=['POST'])
def add_user():  # put application's code here
    req_data = request.get_json()
    """
    {
        'firstname': 'juhani',
        'password': 'salasana',
        'lastname': 'kuru',
        'username': 'juhani.kuru'
    }
    
    """

    with mysql.connector.connect(user='root', password='', host='localhost', database='sovelluskehykset_bad1') as con:
        with con.cursor() as cur:
            cur.execute(
                'INSERT INTO users(firstname, lastname, username) VALUES(%s, %s, %s)',
                (req_data['firstname'], req_data['lastname'], req_data['username']))

            con.commit()
            return jsonify({
                'id': cur.lastrowid,
                'username': req_data['username'],
                'firstname': req_data['firstname'],
                'lastname': req_data['lastname']

            })


if __name__ == '__main__':
    app.run()
