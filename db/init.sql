-- Payments table
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status VARCHAR(20) NOT NULL,
    customer_phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notifications table
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    payment_id INTEGER REFERENCES payments(id),
    phone_number VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample payments data
INSERT INTO payments (amount, currency, status, customer_phone) VALUES
(99.99, 'USD', 'completed', '+1234567890'),
(150.00, 'EUR', 'completed', '+4412345678'),
(75.50, 'GBP', 'failed', '+447123456789'),
(200.00, 'USD', 'pending', '+1987654321'),
(50.00, 'EUR', 'completed', '+4498765432');

-- Sample notifications data
INSERT INTO notifications (payment_id, phone_number, message, status) VALUES
(1, '+1234567890', 'Your payment of $99.99 was successful', 'delivered'),
(2, '+4412345678', 'Your payment of €150.00 was successful', 'delivered'), 
(3, '+447123456789', 'Your payment of £75.50 failed', 'sent'),
(4, '+1987654321', 'Your payment of $200.00 is being processed', 'failed'),
(5, '+4498765432', 'Your payment of €50.00 was successful', 'delivered');