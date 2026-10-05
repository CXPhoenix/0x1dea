from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys

directory = str(Path(sys.argv[1]).resolve())
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs): super().__init__(*args, directory=directory, **kwargs)
    def translate_path(self, path):
        result = super().translate_path(path)
        if not Path(result).exists() and Path(result + '.html').is_file(): return result + '.html'
        return result

print(f'Built static surface {directory} on loopback 127.0.0.1:{sys.argv[2]}', flush=True)
ThreadingHTTPServer(('127.0.0.1', int(sys.argv[2])), Handler).serve_forever()
