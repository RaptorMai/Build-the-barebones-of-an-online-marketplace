# Shopify Summer Intern Challenge 2019

A Django REST API of the barebones of a an online marketplace  for Shopify 2019 summer intern challenge. 
<br>
<br>

### Interactive APIs document
You can find the **interactive document** of APIs here:  
https://raptormai.github.io/swagger-docs-shopify-intern-2019/

### Features

#### Product:
1. Query all products
2. Query available products
3. Query a product by id
4. Purchased a product by id
     * Product with zero inventory can't be purchased
     
#### Cart
1. Add product with quantity to cart, login required
     * Negative quantity can't be add
2. Show cart, login required
3. Check out cart, login requried
     * May have concurrency
     * Use ```with transaction.atomic()``` in Django to deal with it
     * Product with quantity exceeds the available inventory count can't be purchased
     * Product inventory will not reduce until the transaction completed
4. Remove item from cart, login required

#### Security
1. Access control
    * Only authenticated users are allowed to access his/her cart
    * The user can only access his/her cart but not others
2. Some input validations have been implement
3. Only provide HTTPS endpoints
4. Restrict HTTP methods
    *Each API has specific HTTP methods
    *Reject all requests not matching Status code 405 
5. CORS
    *Use package ```corsheaders``` to handle cross-origin resource sharing
6. Each API has HTTP Return Code


### Run it locally
1. Install python3.6 and pip
2. Create a virtual enviroment:
```
python3 -m venv myvenv
```
3. Clone the project
```
git clone https://github.com/RaptorMai/Build-the-barebones-of-an-online-marketplace/
```
4. Install the required package
```
pip install requirement.txt
```
5. Run a PostgreSQL database on your own computer  
Detail can be found at:https://www.postgresql.org/  
The database name should be "shopify_back" and run at localhost with port 5432 

6. Migrate the database
```
python manage.py migrate
```

7. Now you can launch the server
```
python manage.py runserver


