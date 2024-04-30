"""
Module 3: Main
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    register user
    """
    payload = {"email": email, "password": password}
    res = requests.post("http://127.0.0.1:5000/users", data=payload)
    if res.status_code == requests.codes.ok:
        assert (res.status_code == 200)
        assert (res.json() == {"email": email,
                "message": "user created"})
    else:
        assert (res.status_code == 400)
        assert (res.json() == {"message":
                "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """
    login with wrong password check
    """
    payload = {"email": email, "password": password}
    res = requests.post("http://127.0.0.1:5000/sessions", data=payload)
    if res.status_code != 200:
        assert (res.status_code == 401)


def log_in(email: str, password: str) -> str:
    """
    log in with correct password
    """
    payload = {"email": email, "password": password}
    res = requests.post("http://127.0.0.1:5000/sessions", data=payload)
    if res.status_code == requests.codes.ok:
        assert (res.status_code == 200)
        assert (res.json == {"email": email, "message": "logged in"})
        cookie = res.cookies.get("session_id")
        return cookie


def profile_unlogged() -> None:
    """
    check if profile is unlogged
    """
    res = requests.get("http://127.0.0.1:5000/profile")
    assert(res.status_code == 403)


def profile_logged(session_id: str) -> None:
    """
    chekc that use is logged in
    """
    cookie = {"session_id": session_id}
    res = requests.get("http://127.0.0.1:5000/profile", cookies=cookie)
    assert (res.status_code == 200)


def log_out(session_id: str) -> None:
    """
    log out user
    """
    cookie = {"session_id": session_id}
    res = requests.delete("http://127.0.0.1:5000/sessions", cookies=cookie)
    if res.status_code == 302:
        assert (res.json() == {"message": "Bienvenue"})
        assert (res.url == 'http://127.0.0.1:5000/')
    else:
        assert (res.status_code == 200)


def reset_password_token(email: str) -> str:
    """
    reset password token
    """
    payload = {"email": email}
    res = requests.post("http://127.0.0.1:5000/reset_password", data=payload)
    if res.status_code == requests.codes.ok:
        assert (res.status_code == 200)
        reset_token = res.json().get("reset_token")
        assert (res.json() == {"email": email, "reset_token": reset_token})
        return reset_token
    else:
        assert (res.status_code == 401)


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    update password
    """
    payload = {"email": email,
               "password": new_password,
               "reset_token": reset_token}
    res = requests.put("http://127.0.0.1:5000/reset_password", data=payload)
    if res.status_code == requests.codes.ok:
        assert (res.status_code == 200)
        assert(res.json() ==
               {"email": email, "message": "Password updated"})
    else:
        assert(res.status_code == 403)


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
