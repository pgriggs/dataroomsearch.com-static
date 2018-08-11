import os
from flask import Flask, render_template, url_for, json, request
from flask_assets import Environment, Bundle
from flask_share import Share

from app import app

# load social sharing
share = Share()
share.init_app(app)
# Tell flask-assets where to look for our coffeescript and sass files.
assets = Environment(app)

custom_css = Bundle('sass/main.scss',
            filters='scss', output='template/css/custom.css')
assets.register('custom_css', custom_css)

vendor_css = Bundle('css/milligram.min.css',
            output='template/css/vendor.css')
assets.register('vendor_css', vendor_css)


@app.route('/')
def index():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = open(os.path.join(SITE_ROOT, "static/data", "products.json"), "r")
    data = json.load(json_url)
    return render_template("index.html", products=data)

@app.route('/virtual-data-room-provider/<provider>')
def about(provider):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = open(os.path.join(SITE_ROOT, "static/data", "products.json"), "r")
    data = json.load(json_url)
    return render_template("product.html", products=data, provider=provider)