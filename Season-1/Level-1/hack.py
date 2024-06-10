import unittest
import code as c

class TestOnlineStore(unittest.TestCase):

    # Tricks the system and walks away with 1 television, despite valid payment & reimbursement
    # code.py

    class Item:
        def __init__(self, type, description, amount, quantity):
            self.type = type
            self.description = description
            self.amount = amount
            self.quantity = quantity

    class Order:
        def __init__(self, id, items):
            self.id = id
            self.items = items

    def validorder(order):
        total_amount = 0
        for item in order.items:
            total_amount += item.amount * item.quantity
        if total_amount == 0:
            return 'Order ID: {} - Full payment received!'.format(order.id)
        elif total_amount < 0:
            return 'Order ID: {} - Payment imbalance: ${:.2f}'.format(order.id, total_amount)
        else:
            return 'Order ID: {} - Total amount payable for an order exceeded'.format(order.id)

    # Valid payments that should add up correctly, but do not
    def test_7(self):
        small_item = c.Item(type='product', description='accessory', amount=3.3, quantity=1)
        payment_1 = c.Item(type='payment', description='invoice_5_1', amount=1.1, quantity=1)
        payment_2 = c.Item(type='payment', description='invoice_5_2', amount=2.2, quantity=1)
        order_5 = c.Order(id='5', items=[small_item, payment_1, payment_2])
        self.assertEqual(c.validorder(order_5), 'Order ID: 5 - Payment imbalance: $-0.44')

    # The total amount payable in an order should be limited
    def test_8(self):
        num_items = 12
        items = [c.Item(type='product', description='tv', amount=99999, quantity=num_items)]
        for i in range(num_items):
            items.append(c.Item(type='payment', description='invoice_' + str(i), amount=99999, quantity=1))
        order_1 = c.Order(id='1', items=items)
        self.assertEqual(c.validorder(order_1), 'Order ID: 1 - Total amount payable for an order exceeded')
    
        # Put payments before products
        items = items[1:] + [items[0]]
        order_2 = c.Order(id='2', items=items)
        self.assertEqual(c.validorder(order_2), 'Order ID: 2 - Total amount payable for an order exceeded')

if __name__ == '__main__':
    unittest.main()