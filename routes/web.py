from flask import Blueprint, render_template, request, redirect, url_for, flash



web_bp = Blueprint(
    "web",
    __name__
)


@web_bp.route("/convite")
def convite():
    return render_template("invitation.html")