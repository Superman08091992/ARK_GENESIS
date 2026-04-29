import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .status import RuntimeStatusReader

DEFAULT_BIND = '127.0.0.1'
DEFAULT_PORT = 8081
DEFAULT_RUNTIME_ROOT = Path('/opt/ark')

class ARKStatusHandler(BaseHTTPRequestHandler):
    runtime_root = DEFAULT_RUNTIME_ROOT

    def _send_json(self, status_code, payload):
        body = json.dumps(payload, sort_keys=True, indent=2).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/health':
            self._send_json(200, {'ok': True, 'service': 'ark-local-api'})
            return
        if path == '/status':
            self._send_json(200, RuntimeStatusReader(self.runtime_root).read_status())
            return
        self._send_json(404, {'ok': False, 'error': 'not found'})

    def log_message(self, format, *args):
        return

def make_server(host=DEFAULT_BIND, port=DEFAULT_PORT, runtime_root=DEFAULT_RUNTIME_ROOT):
    class Handler(ARKStatusHandler):
        pass
    Handler.runtime_root = Path(runtime_root)
    return ThreadingHTTPServer((host, int(port)), Handler)

def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description='ARK local status API')
    parser.add_argument('--host', default=DEFAULT_BIND)
    parser.add_argument('--port', type=int, default=DEFAULT_PORT)
    parser.add_argument('--runtime-root', default=str(DEFAULT_RUNTIME_ROOT))
    args = parser.parse_args(argv)
    server = make_server(args.host, args.port, Path(args.runtime_root))
    print(f'ARK local API listening on http://{args.host}:{args.port}')
    server.serve_forever()

if __name__ == '__main__':
    main()
