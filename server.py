
import json
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import os

DB_NAME = 'meals.db'

class SimpleHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type='application/json'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/':
            self._set_headers('text/html')
            with open('templates/index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif parsed_path.path == '/api/recipes':
            self._set_headers()
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT meals.name, meals.id, 
                       CASE WHEN COUNT(CASE WHEN ingredients.name IN ('chicken', 'salmon', 'turkey', 'beef') THEN 1 END) > 0 
                       THEN 0 ELSE 1 END as is_veg
                FROM meals
                LEFT JOIN ingredients ON meals.id = ingredients.meal_id
                GROUP BY meals.id
            """)
            rows = cursor.fetchall()
            conn.close()

            recipe_list = []
            for name, _, is_veg in rows:
                lower = name.lower()
                if 'breakfast' in lower or 'oat' in lower or 'egg' in lower:
                    type_guess = 'breakfast'
                elif 'salad' in lower or 'lunch' in lower:
                    type_guess = 'lunch'
                elif 'snack' in lower or 'toast' in lower or 'parfait' in lower:
                    type_guess = 'snacks'
                else:
                    type_guess = 'dinner'
                recipe_list.append({
                    'name': name,
                    'type': type_guess,
                    'isVegetarian': bool(is_veg)
                })

            self.wfile.write(json.dumps(recipe_list).encode('utf-8'))

        elif parsed_path.path.startswith('/static/'):
            file_path = '.' + parsed_path.path
            if os.path.isfile(file_path):
                self._set_headers('text/csv')
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())

        else:
            self.send_error(404, "File Not Found")

def run(server_class=HTTPServer, handler_class=SimpleHandler, port=8000):
    print(f'Starting server at http://localhost:{port}')
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
