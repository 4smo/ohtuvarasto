"""Routes for the warehouse web application."""
from flask import render_template, request, redirect, url_for
from web.models import db, Warehouse, Item


def register_routes(app):
    """Register all routes for the application."""
    register_warehouse_routes(app)
    register_item_routes(app)


def register_warehouse_routes(app):  # pylint: disable=too-many-statements
    """Register warehouse-related routes."""

    @app.route('/')
    def index():
        """Display list of all warehouses."""
        warehouses = Warehouse.query.all()
        return render_template('index.html', warehouses=warehouses)

    @app.route('/warehouse/create', methods=['POST'])
    def create_warehouse():
        """Create a new warehouse."""
        name = request.form.get('name', '').strip()
        if name:
            warehouse = Warehouse(name=name)
            db.session.add(warehouse)
            db.session.commit()
        return redirect(url_for('index'))

    @app.route('/warehouse/<int:warehouse_id>/delete', methods=['POST'])
    def delete_warehouse(warehouse_id):
        """Delete a warehouse and all its items."""
        warehouse = db.session.get(Warehouse, warehouse_id)
        if warehouse:
            db.session.delete(warehouse)
            db.session.commit()
        return redirect(url_for('index'))

    @app.route('/warehouse/<int:warehouse_id>')
    def view_warehouse(warehouse_id):
        """View a specific warehouse and its items."""
        warehouse = db.session.get(Warehouse, warehouse_id)
        if not warehouse:
            return redirect(url_for('index'))
        return render_template('warehouse.html', warehouse=warehouse)


def register_item_routes(app):
    """Register item-related routes."""

    @app.route('/warehouse/<int:warehouse_id>/item/add', methods=['POST'])
    def add_item(warehouse_id):
        """Add an item to a warehouse."""
        warehouse = db.session.get(Warehouse, warehouse_id)
        if warehouse:
            save_item(warehouse_id)
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))

    @app.route(
        '/warehouse/<int:warehouse_id>/item/<int:item_id>/delete',
        methods=['POST']
    )
    def delete_item(warehouse_id, item_id):
        """Remove an item from a warehouse."""
        item = db.session.get(Item, item_id)
        if item and item.warehouse_id == warehouse_id:
            db.session.delete(item)
            db.session.commit()
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


def save_item(warehouse_id):
    """Save an item to the database."""
    name = request.form.get('name', '').strip()
    quantity = parse_quantity(request.form.get('quantity', 0))
    if name and quantity > 0:
        item = Item(name=name, quantity=quantity, warehouse_id=warehouse_id)
        db.session.add(item)
        db.session.commit()


def parse_quantity(value):
    """Parse quantity from form input."""
    try:
        return int(value)
    except ValueError:
        return 0
