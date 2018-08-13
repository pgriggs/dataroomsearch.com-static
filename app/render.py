import os
from flask import Flask, render_template, url_for, json, request

from flask_assets import Environment, Bundle
from flask_share import Share
from PIL import Image

app = Flask(__name__, instance_relative_config=True)

# load social sharing
share = Share()
share.init_app(app)
# Tell flask-assets where to look for our coffeescript and sass files.
assets = Environment(app)

custom_css = Bundle('sass/main.scss',
            filters='scss', output='templates/css/custom.css')
assets.register('custom_css', custom_css)

vendor_css = Bundle('css/milligram.min.css',
            output='templates/css/vendor.css')
assets.register('vendor_css', vendor_css)


if __name__ == "__main__":
    with app.app_context():
        product_schema = {"@context": "http://schema.org","@type": "Product"}
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = open(os.path.join(SITE_ROOT, "static/data", "products.json"), "r")
        data = json.load(json_url)
        # compress images and move to build directory
        for filename in os.listdir("app/static/images/"):
            if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                im = Image.open("app/static/images/"+filename)
                im_rgb = im.convert('RGB')
                im_rgb.save("app/rendered_pages/images/"+filename,optimize=True,quality=60)
            else:
                im = Image.open("app/static/images/"+filename)
                im.save("app/rendered_pages/images/"+filename)
        for index, product in enumerate(data['data']):
            provider = product['name']
            url_slug = product['urlSlug']
            relatedProducts = []
            product_schema['image'] = product['logoURL']
            product_schema['url'] = "https://dataroomsearch.com/" + product['urlSlug']
            product_schema['name'] = product['name']
            product_schema['aggregateRating'] = {"@type": "AggregateRating"}
            product_schema['aggregateRating']['ratingValue'] = product['avg_review_rating']
            product_schema['aggregateRating']['reviewCount'] = product['num_reviews']
            product_schema['offers'] = {"@type": "Offer"}
            product_schema['offers']['price'] = product['price']
            product_schema['offers']['priceCurrency'] = "USD"
            if product['urlSlug'] == url_slug and index < len(data['data'])-3:
                relatedProducts.append(data['data'][index+1])
                relatedProducts.append(data['data'][index+2])
                relatedProducts.append(data['data'][index+3])
            if product['urlSlug'] == url_slug and index >= len(data['data'])-3:
                relatedProducts.append(data['data'][index-1])
                relatedProducts.append(data['data'][index-2])
                relatedProducts.append(data['data'][index-3])
            rendered = render_template('product.html', products=data, provider=provider, product_schema=json.dumps(product_schema), relatedProducts=relatedProducts, url_slug=url_slug)
            Html_file= open("app/rendered_pages/virtual-data-room-provider/" + url_slug + ".html","wb")
            Html_file.write(rendered.encode('utf-8'))
            Html_file.close()
            print(rendered)
            rendered = render_template('product-amp.html', products=data, provider=provider, product_schema=json.dumps(product_schema), relatedProducts=relatedProducts, url_slug=url_slug)
            Html_file= open("app/rendered_pages/amp/virtual-data-room-provider/" + url_slug + ".html","wb")
            Html_file.write(rendered.encode('utf-8'))
            Html_file.close()
            print(rendered)
        rendered_index = render_template("index.html", products=data)
        Html_file= open("app/rendered_pages/index.html","wb")
        Html_file.write(rendered_index.encode('utf-8'))
        Html_file.close()
        print(rendered_index)
        rendered_index = render_template("index-amp.html", products=data)
        Html_file= open("app/rendered_pages/amp/home.html","wb")
        Html_file.write(rendered_index.encode('utf-8'))
        Html_file.close()
        print(rendered_index)