from tkinter import messagebox
import win32api
from flask import Blueprint, render_template, redirect, request

submain = Blueprint("sec", __name__, static_folder="static", template_folder="templates")


@submain.route("/paydet", methods=["POST", "GET"])
def usr():
    if request.method == "POST":
            name = request.form['nm']
            eml = request.form['eml']
            amt = request.form['amt']
            print("Gotcha!!!!")

            print("name=", name, "Amt=", amt)
            return render_template("payment.html", name=name)

    else:
        print("method is of type:" + request.method)
        # return render_template("paydet.html")

    return render_template("paydet.html")






@submain.route("/pay", methods=["POST", "GET"])
def mny():
    if request.method == "post":
        return render_template("payment.html")
    else:
        return "Not a post Method"


@submain.route("/dial", methods=["POST", "GET"])
def suc():
    return render_template("dial.html")
