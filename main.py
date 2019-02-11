from flask import Flask, request, redirect, render_template
from flask_squlalchemy import SQLAlchemy

app = Flask(__name__)
app.config('DEBUG') = True

