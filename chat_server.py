from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
import openai

openai.api_key = "Your API key"

class ChatHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)
        user_input = params['user_input'][0]

        response = self.chat_with_gpt(user_input)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_data = {'response': response}
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404)

    def chat_with_gpt(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        return response['choices'][0]['message']['content'].strip()

if __name__ == '__main__':
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, ChatHandler)
    host, port = httpd.server_address
    print(f'Starting the server on http://{host}:{port}/')
    httpd.serve_forever()


    