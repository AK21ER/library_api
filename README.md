📖 API Documentation – Library Management System

This API allows users to register, login, manage books, borrow books, and return books.
All routes are tested via Postman.

🔑 Authentication Endpoints
1. Register a New User

POST /api/accounts/register/
Request Body:

{
    "username": "john",
    "email": "john@example.com",
    "password": "mypassword123",
    "password2": "mypassword123"
}


2. Login User (JWT Authentication)

POST /api/accounts/login/
Request Body:

{
  "username": "john_doe",
  "password": "password123"
}

3. Get All Books

GET /api/books/
Headers:

Authorization: Bearer <your-access-token>


4. Add New Book

POST /api/books/
Headers:

Authorization: Bearer <your-access-token>


Request Body:

{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "isbn": "9780743273565",
  "published_year": 1925
}



5. Get Single Book by ID

GET /api/books/1/
Headers:

Authorization: Bearer <your-access-token>



6. Update Book

PUT /api/books/1/
Headers:

Authorization: Bearer <your-access-token>


Request Body:

{
  "title": "The Great Gatsby - Updated",
  "author": "F. Scott Fitzgerald",
  "isbn": "9780743273565",
  "published_year": 1926,
  "published_date" : 20/02/1926
}

7. Delete Book

DELETE /api/books/1/
Headers:

Authorization: Bearer <your-access-token>



📖 Borrow Endpoints
8. Borrow a Book

POST /api/borrows/
Headers:

Authorization: Bearer <your-access-token>


Request Body:

{
 
  "book_id": 1,
 
}



9. Return a Book

PUT /api/borrows/1/
Headers:

Authorization: Bearer <your-access-token>


Request Body:

{
  "user": 1,
  "book": 1,
  "borrow_date": "2025-08-27",
  "return_date": "2025-09-01"
}


👥 User Management Endpoints
10. Get All Users

GET /api/users/
Headers:

Authorization: Bearer <your-access-token>



11. Get Single User by ID

GET /api/users/1/
Headers:

Authorization: Bearer <your-access-token>