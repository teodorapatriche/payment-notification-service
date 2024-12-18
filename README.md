# payment-notification-service
## Payment and Notification Service

1) Payment Service: Handles payment processing.

2) Notification Service: Sends SMS notifications asynchronously using a Redis-based job queue.

## FEATURES

- Payment Processing: Integrates with the Stripe API to handle secure payments.

- Notification System: Sends SMS notifications asynchronously to users upon successful payment.

- Microservices Architecture: Separate services for payment and notification functionalities.

- Dockerized Deployment: Services and dependencies run in containers individually and together.

- Async Job Processing: Uses Redis and RQ (Redis Queue) for background task management.

- Basic logging

## TODOs

- [ ] store secrets
- [ ] integrate with a database to store payment logs
- [ ] add more complex logging to monitor requests
- [ ] explore deployment options

