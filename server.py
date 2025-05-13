import json
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import os

DB_NAME = 'meals.db'

# Initialize the database and tables
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY(meal_id) REFERENCES meals(id)
        )
    ''')
    conn.commit()
    conn.close()

class SimpleHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        # Handle CORS preflight
        self._set_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path == '/':
            self._set_headers(content_type='text/html')
            with open('Home.html', 'rb') as f:
                self.wfile.write(f.read())

        elif path == '/api/recipes':
            # Optional filtering by type or vegetarian flag
            type_filter = qs.get('type', [None])[0]
            veg_filter = qs.get('vegetarian', [None])[0]

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.id, m.name,
                       CASE WHEN COUNT(CASE WHEN i.name IN ('chicken','salmon','turkey','beef') THEN 1 END) > 0
                            THEN 0 ELSE 1 END as is_veg
                FROM meals m
                LEFT JOIN ingredients i ON m.id = i.meal_id
                GROUP BY m.id
            """)
            items = []
            for mid, name, is_veg in cursor.fetchall():
                lower = name.lower()
                if any(x in lower for x in ('breakfast','oat','egg')):
                    type_guess = 'breakfast'
                elif any(x in lower for x in ('salad','lunch')):
                    type_guess = 'lunch'
                elif any(x in lower for x in ('snack','toast','parfait')):
                    type_guess = 'snacks'
                else:
                    type_guess = 'dinner'

                if type_filter and type_guess != type_filter:
                    continue
                if veg_filter is not None and str(is_veg) != veg_filter:
                    continue

                items.append({
                    'id': mid,
                    'name': name,
                    'type': type_guess,
                    'isVegetarian': bool(is_veg)
                })
            conn.close()

            self._set_headers()
            self.wfile.write(json.dumps(items).encode('utf-8'))

        elif path.startswith('/api/recipes/'):  # GET single recipe by ID
            try:
                rid = int(path.rsplit('/', 1)[-1])
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM meals WHERE id = ?", (rid,))
                row = cursor.fetchone()
                if not row:
                    self.send_error(404, 'Recipe not found')
                    return

                name = row[0]
                cursor.execute("SELECT name FROM ingredients WHERE meal_id = ?", (rid,))
                ingredients = [r[0] for r in cursor.fetchall()]
                conn.close()

                self._set_headers()
                self.wfile.write(json.dumps({
                    'id': rid,
                    'name': name,
                    'ingredients': ingredients
                }).encode('utf-8'))
            except ValueError:
                self.send_error(400, 'Invalid recipe ID')

        elif path.startswith('/static/'):
            file_path = '.' + path
            if os.path.isfile(file_path):
                ct = 'text/plain'
                if file_path.endswith('.css'):
                    ct = 'text/css'
                elif file_path.endswith('.js'):
                    ct = 'application/javascript'

                self._set_headers(content_type=ct)
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, 'File Not Found')

        else:
            self.send_error(404, 'Not Found')

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/recipes':
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length))
            name = data.get('name')
            ingredients = data.get('ingredients', [])

            if not name:
                self.send_error(400, 'Recipe name is required')
                return

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO meals (name) VALUES (?)", (name,))
            meal_id = cursor.lastrowid
            for ing in ingredients:
                cursor.execute("INSERT INTO ingredients (meal_id, name) VALUES (?, ?)", (meal_id, ing))
            conn.commit()
            conn.close()

            self._set_headers(status=201)
            self.wfile.write(json.dumps({'id': meal_id}).encode('utf-8'))
        else:
            self.send_error(404, 'Not Found')


def run(server_class=HTTPServer, handler_class=SimpleHandler, port=8000):
    init_db()
    print(f'Starting server at http://localhost:{port}')
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
