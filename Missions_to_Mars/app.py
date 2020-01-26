from flask import Flask, render_template, redirect
# Import scrape_mars
import scrape_mars

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017/mission'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Set route
@app.route("/")
def index():
    mars = client.missionDb.mars.find_one()
    return render_template("index.html", mars = mars)

# Scrape 
@app.route("/scrape")
def scrape():
    mars = client.missionDb.mars 
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)