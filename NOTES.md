# Development Notes

## Ecommerce MVP

1. User Management - Restration, Login and JWT
2. Product Catalog - CRUD operations for products (Admin only for write/delete, public for read)
3. Shopping Cart - Adding, removing, and updating items in a temporary state
4. Order & Checkout - converting cart into an order and calculating totals

## Commands

- For async alembic with asyncpg for postgresql and asyncio;
  - alembic init -t async alembic
  - alembic revision --autogenerate -m "Initial migration"
  - alembic upgrade head

# Extras
