import hashlib
import hmac
import secrets

try:
    from werkzeug.security import generate_password_hash as _wz_gen, check_password_hash as _wz_check
    HAS_WERKZEUG = True
except ImportError:
    HAS_WERKZEUG = False


def generate_password_hash(password: str) -> str:
    """Gera hash seguro da senha compatível com Werkzeug scrypt."""
    if HAS_WERKZEUG:
        return _wz_gen(password)
    salt = secrets.token_urlsafe(12)[:16]
    n, r, p = 32768, 8, 1
    dk = hashlib.scrypt(
        password.encode('utf-8'),
        salt=salt.encode('utf-8'),
        n=n,
        r=r,
        p=p,
        maxmem=64 * 1024 * 1024,
        dklen=64,
    )
    return f"scrypt:{n}:{r}:{p}${salt}${dk.hex()}"


def check_password_hash(pwhash: str, password: str) -> bool:
    """Verifica senha contra hash scrypt/pbkdf2 do Werkzeug ou fallback nativo."""
    if not pwhash or not password:
        return False
    if HAS_WERKZEUG:
        try:
            return _wz_check(pwhash, password)
        except Exception:
            pass

    try:
        parts = pwhash.split('$')
        if len(parts) != 3:
            return hmac.compare_digest(pwhash, password)
        method_info, salt, hash_val = parts
        if method_info.startswith('scrypt:'):
            _, n_str, r_str, p_str = method_info.split(':')
            n, r, p = int(n_str), int(r_str), int(p_str)
            dk = hashlib.scrypt(
                password.encode('utf-8'),
                salt=salt.encode('utf-8'),
                n=n,
                r=r,
                p=p,
                maxmem=64 * 1024 * 1024,
                dklen=len(bytes.fromhex(hash_val)),
            )
            return hmac.compare_digest(dk.hex(), hash_val)
    except Exception:
        return False
    return False
