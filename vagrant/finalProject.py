from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__, template_folder='templates')

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
  print(items)
  return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
  Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
  return jsonify(Menu_Item=Menu_Item.serialize)

@app.route('/restaurant/JSON')
def restaurantsJSON():
  restaurants = session.query(Restaurant).all()
  return jsonify(restaurants=[r.serialize for r in restaurants])

# Show all restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
  restaurants = session.query(Restaurant).all()
  return render_template("restaurants.html", restaurants=restaurants)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
  return render_template("menu.html", restaurant=restaurant, items=items)

@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
  if request.method == 'POST':
    newRestaurant = Restaurant(name=request.form['name'])
    session.add(newRestaurant)
    session.commit()
    flash("New Restaurant created!")
    return redirect(url_for('showRestaurants'))
  else:
    return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
  editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  if request.method == 'POST':
    if request.form['name']:
      editedRestaurant.name = request.form['name']
      return redirect(url_for('showRestaurants'))
  else:
    return render_template('editRestaurant.html', restaurant=editedRestaurant)

@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
  restaurantToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
  if request.method == 'POST':
    session.delete(restaurantToDelete)
    session.commit()
    flash("Restaurant Successfully Deleted!")
    return redirect(url_for('showRestaurants', restaurant_id=restaurant_id))
  else:
    return render_template('deleteRestaurant.html', restaurant=restaurantToDelete)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
  return render_template('menu.html', items=items, restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/new',  methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
  if request.method == 'POST':
    newItem = MenuItem(name=request.form['name'], description=request.form[
      'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
    session.add(newItem)
    session.commit()
    flash("Menu Item Created!")
    return redirect(url_for('showMenu', restaurant_id=restaurant_id))
  else:
    return render_template('newMenuItem.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
  editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
  if request.method == 'POST':
    if request.form['name']:
      editedItem.name = request.form['name']
    if request.form['description']:
      editedItem.description = request.form['name']
    if request.form['price']:
      editedItem.price = request.form['price']
    if request.form['course']:
      editedItem.course = request.form['course']
    session.add(editedItem)
    session.commit()
    flash("Menu Item Successfully Edited")
    return redirect(url_for('showMenu', restaurant_id=restaurant_id))
  else:
    return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
  itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
  if request.method == 'POST':
    session.delete(itemToDelete)
    session.commit()
    return redirect(url_for('showMenu', restaurant_id=restaurant_id))
  else:
    return render_template('deleteMenuItem.html', item=itemToDelete)


if __name__ == "__main__":
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = "0.0.0.0")
