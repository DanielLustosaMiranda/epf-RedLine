import json
import os
import uuid
from http.cookies import SimpleCookie

try:
    from beaker.middleware import SessionMiddleware as BeakerSessionMiddleware
    HAS_BEAKER = True
except ImportError:
    HAS_BEAKER = False


class FileSession(dict):
    """Sessão persistida em arquivo compatível com a interface do Beaker."""

    def __init__(self, data_dir, session_id=None):
        super().__init__()
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.id = session_id or uuid.uuid4().hex
        self.invalidated = False
        self._load()

    @property
    def _filepath(self):
        safe_id = ''.join(c for c in self.id if c.isalnum())
        return os.path.join(self.data_dir, f"sess_{safe_id}.json")

    def _load(self):
        if os.path.exists(self._filepath):
            try:
                with open(self._filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.update(data)
            except Exception:
                pass

    def save(self):
        if self.invalidated:
            return
        os.makedirs(self.data_dir, exist_ok=True)
        try:
            with open(self._filepath, 'w', encoding='utf-8') as f:
                json.dump(dict(self), f, ensure_ascii=False)
        except Exception:
            pass

    def delete(self):
        self.clear()
        self.invalidated = True
        if os.path.exists(self._filepath):
            try:
                os.remove(self._filepath)
            except OSError:
                pass


class FallbackSessionMiddleware:
    """Middleware WSGI leve compatível com beaker.session quando Beaker não está instalado."""

    COOKIE_NAME = 'redline_session_id'

    def __init__(self, app, config=None):
        self.app = app
        self.config = config or {}
        self.data_dir = self.config.get('session.data_dir', './data/sessions')
        os.makedirs(self.data_dir, exist_ok=True)

    def __call__(self, environ, start_response):
        cookie_header = environ.get('HTTP_COOKIE', '')
        cookie = SimpleCookie()
        if cookie_header:
            try:
                cookie.load(cookie_header)
            except Exception:
                pass

        session_id = None
        if self.COOKIE_NAME in cookie:
            session_id = cookie[self.COOKIE_NAME].value

        session = FileSession(self.data_dir, session_id=session_id)
        environ['beaker.session'] = session

        def custom_start_response(status, headers, exc_info=None):
            if session.invalidated:
                headers.append(
                    ('Set-Cookie', f'{self.COOKIE_NAME}=; Path=/; Max-Age=0; HttpOnly')
                )
            else:
                session.save()
                headers.append(
                    ('Set-Cookie', f'{self.COOKIE_NAME}={session.id}; Path=/; Max-Age=86400; HttpOnly')
                )
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)


def create_session_middleware(app, session_opts):
    if HAS_BEAKER:
        return BeakerSessionMiddleware(app, session_opts)
    return FallbackSessionMiddleware(app, session_opts)
