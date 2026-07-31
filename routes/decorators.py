from functools import wraps
from flask import session, redirect, url_for, flash


def admin_required(view):

    @wraps(view)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        if session.get("role") != "administrator":
            flash("Acesso permitido apenas para administradores.", "danger")
            return redirect(url_for("web.patient_dashboard"))

        return view(*args, **kwargs)

    return wrapper