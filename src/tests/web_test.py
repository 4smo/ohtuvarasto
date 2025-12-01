"""Test module for the warehouse web application."""
import unittest
from web.app import create_app
from web.models import db, Warehouse, Item


class TestWebApp(unittest.TestCase):
    """Test class for web application functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
        })
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down test fixtures."""
        with self.app.app_context():
            db.drop_all()

    def test_index_shows_empty_warehouse_list(self):
        """Test that index shows empty warehouse list."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouses', response.data)
        self.assertIn(b'No warehouses yet.', response.data)

    def test_create_warehouse(self):
        """Test creating a new warehouse."""
        response = self.client.post(
            '/warehouse/create',
            data={'name': 'Test Warehouse'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Warehouse', response.data)

    def test_create_warehouse_empty_name(self):
        """Test creating warehouse with empty name does nothing."""
        self.client.post('/warehouse/create', data={'name': ''})
        response = self.client.get('/')
        self.assertIn(b'No warehouses yet.', response.data)

    def test_delete_warehouse(self):
        """Test deleting a warehouse."""
        self.client.post('/warehouse/create', data={'name': 'To Delete'})
        with self.app.app_context():
            warehouse = Warehouse.query.first()
            warehouse_id = warehouse.id
        response = self.client.post(
            f'/warehouse/{warehouse_id}/delete',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No warehouses yet.', response.data)

    def test_delete_nonexistent_warehouse(self):
        """Test deleting nonexistent warehouse redirects to index."""
        response = self.client.post(
            '/warehouse/999/delete',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_view_warehouse(self):
        """Test viewing a specific warehouse."""
        self.client.post('/warehouse/create', data={'name': 'My Warehouse'})
        with self.app.app_context():
            warehouse = Warehouse.query.first()
            warehouse_id = warehouse.id
        response = self.client.get(f'/warehouse/{warehouse_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Warehouse', response.data)
        self.assertIn(b'No items in this warehouse.', response.data)

    def test_view_nonexistent_warehouse_redirects(self):
        """Test viewing nonexistent warehouse redirects to index."""
        response = self.client.get('/warehouse/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouses', response.data)

    def test_add_item_to_warehouse(self):
        """Test adding an item to a warehouse."""
        self.client.post('/warehouse/create', data={'name': 'Items Warehouse'})
        with self.app.app_context():
            warehouse = Warehouse.query.first()
            warehouse_id = warehouse.id
        response = self.client.post(
            f'/warehouse/{warehouse_id}/item/add',
            data={'name': 'Test Item', 'quantity': '5'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Item', response.data)
        self.assertIn(b'Quantity: 5', response.data)

    def test_add_item_invalid_quantity(self):
        """Test adding item with invalid quantity."""
        self.client.post('/warehouse/create', data={'name': 'Warehouse'})
        with self.app.app_context():
            warehouse = Warehouse.query.first()
            warehouse_id = warehouse.id
        self.client.post(
            f'/warehouse/{warehouse_id}/item/add',
            data={'name': 'Bad Item', 'quantity': 'abc'}
        )
        response = self.client.get(f'/warehouse/{warehouse_id}')
        self.assertIn(b'No items in this warehouse.', response.data)

    def test_add_item_zero_quantity(self):
        """Test adding item with zero quantity does nothing."""
        self.client.post('/warehouse/create', data={'name': 'Warehouse'})
        with self.app.app_context():
            warehouse = Warehouse.query.first()
            warehouse_id = warehouse.id
        self.client.post(
            f'/warehouse/{warehouse_id}/item/add',
            data={'name': 'Zero Item', 'quantity': '0'}
        )
        response = self.client.get(f'/warehouse/{warehouse_id}')
        self.assertIn(b'No items in this warehouse.', response.data)

    def test_delete_item_from_warehouse(self):  # pylint: disable=R0915
        """Test removing an item from a warehouse."""
        self.client.post('/warehouse/create', data={'name': 'Warehouse'})
        with self.app.app_context():
            warehouse = Warehouse.query.first()
            warehouse_id = warehouse.id
        self.client.post(
            f'/warehouse/{warehouse_id}/item/add',
            data={'name': 'To Remove', 'quantity': '3'}
        )
        with self.app.app_context():
            item = Item.query.first()
            item_id = item.id
        response = self.client.post(
            f'/warehouse/{warehouse_id}/item/{item_id}/delete',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No items in this warehouse.', response.data)

    def test_delete_item_wrong_warehouse(self):  # pylint: disable=R0915
        """Test deleting item from wrong warehouse does nothing."""
        self.client.post('/warehouse/create', data={'name': 'Warehouse 1'})
        self.client.post('/warehouse/create', data={'name': 'Warehouse 2'})
        with self.app.app_context():
            warehouse1 = Warehouse.query.first()
            warehouse1_id = warehouse1.id
        self.client.post(
            f'/warehouse/{warehouse1_id}/item/add',
            data={'name': 'Item', 'quantity': '1'}
        )
        with self.app.app_context():
            item = Item.query.first()
            item_id = item.id
        self.client.post(f'/warehouse/999/item/{item_id}/delete')
        with self.app.app_context():
            item = db.session.get(Item, item_id)
            self.assertIsNotNone(item)

    def test_cascade_delete_items_with_warehouse(self):  # pylint: disable=R0915
        """Test that items are deleted when warehouse is deleted."""
        self.client.post('/warehouse/create', data={'name': 'Warehouse'})
        with self.app.app_context():
            warehouse = Warehouse.query.first()
            warehouse_id = warehouse.id
        self.client.post(
            f'/warehouse/{warehouse_id}/item/add',
            data={'name': 'Item 1', 'quantity': '1'}
        )
        self.client.post(
            f'/warehouse/{warehouse_id}/item/add',
            data={'name': 'Item 2', 'quantity': '2'}
        )
        self.client.post(f'/warehouse/{warehouse_id}/delete')
        with self.app.app_context():
            items = Item.query.all()
            self.assertEqual(len(items), 0)

    def test_add_item_to_nonexistent_warehouse(self):
        """Test adding item to nonexistent warehouse."""
        response = self.client.post(
            '/warehouse/999/item/add',
            data={'name': 'Item', 'quantity': '1'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
