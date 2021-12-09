# CS50W Final Project - Capstone

## Description
Design an inventory and sales operations app which allows users to manage products and sales.
Django was used in the backend, and Javascript in the frontend

#### Key features:
- Dashboard: view sales figures and brief reports such as recent sales, top sales, top selling products/categories
- Sales/Orders (main feature): create orders, sales channels and update existing orders/channels
- Customers: create and manage customers
- Products: register and manage products and categories
- Warehouses: register a warehouse and view inventory in each warehouse

#### Specifications:
- Login/logout: using Django's built-in users and authentication system
- Layout: using Bootstrap dashboard [https://getbootstrap.com/docs/5.1/examples/dashboard/]
- Each user can create their own inventory and sales data. They cannot access other users' data.
- Inventory is loaded from the Django backend/admin
- Customers: a new customer is created with three main details - contact, billing and shipping (customer_form.html). The Customer model is split into three ModelForms for ease of displaying on frontend.
    Usually shipping information is the same to billing information, so there is a button that allows them to copy billing details over to shipping details (using javascript inventory.js).
    A list of customers can be viewed with pagination (customer_list.html)
- Sales Orders:
    - Create/Edit a Sales Order: users can create a new sales order (model SalesOrder) for a specific customer which can be selected from a dropdown list of existing customers (sales_order_form.html).
        Orders can be managed by status:
        - Draft: inventory is held but order has not been committed
        - Created: inventory is committed
        - Invoiced: invoice has been issued to the customer
        - Dispatched: items have been shipped out
        - Paid: invoice has been paid
        - Closed: order has been finalised
        When a warehouse is selected from a dropdown list, the product items in this warehouse will become available for users to select from. This is done via javascript by sending query to server and getting a Json response (inventory.js). Available quantity is displayed alongside product name so that users know how many items are available.
        Users can also dynamically add a new item/product to the order. This is done via javascript on the front-end and Django formset on the backend. Items are managed by a separate model SalesItem.
        Order value is calculated dynamically but it is not saved to database as it can be calculated from the SalesOrder and SalesItem tables. It might be good to save it to database in the future if it is used frequently.
        Once a sales order is created/edited, the inventory in the selected warehouse will be updated. This allows users to manage inventory and avoid selling unavailable products.
    - Order List: the order list page shows a list of sales orders (sales_order.html) in a table with a link to each order that enables users to edit that order. Users can search orders by created/invoice date, or by order status. By default, it only shows orders that have not been closed. The 'Reset' button triggers the default view. If users want to see all orders (including 'Closed' ones), they can use the button 'Show All'.
    As orders are listed using Django paginator, the search input needs to be saved so that it can be pre-filled in the next pages. This is done via session. For now, this application does not allow multiple search conditions.
    - Sales Channel: a sales channel (e.g. Retail, Wholesale) can be created and edited (channel_form.html). Available sales channels will be displayed as a dropdown list in the sales order form.
- Products: users register new products and edit them (product_form.html). A list of products can be viewed in a table with basic product details (product.html). The list also uses Django paginator displaying products in multiple pages.
    - Product Category can be created and editted (category_form.html). Each product belongs to a certain category. A category is required when creating a new product.
- Warehouses: similar to Products, users can register and update a warehouse (warehouse_form.html).
    The stock on hand report (or warehouse list) displays all warehouses with the products and quantities they hold (warehouse.html)
- Dashboard: (index.html) shows sales insights such as sales this month or top selling products. This is extracted from multiple tables in database.


## Distinctiveness
This web application allows users to manage sales and inventory. It is distinct from other projects in this course in terms of what it allows users to do. And it is more data intensive with many more models and forms to manage.


## Complexity
- Data structure: this application has many data Models: Product, Customer, SalesOrder, SalesItem, just to name a few.
- As each user has their own data and cannot access others', each Model has been designed with 'user' as a Foreign Key. In order to show data belonging to the current user, the ModelForms must dynamically filter data using queryset in the __init__ method (see references below). E.g. see the model ProductForm which filters Category belonging to the current user.
- The two most complex features in this web application are the 'Sales Order List' with search functionality and 'Create/Edit a Sales Order'.
    - Sales Order List: 
        - In the order table, order values must be displayed. As they are not saved in the database, they are calculated in views and passed on to the frontend.
        - Search input must be preserved in the next pages so session was utilised.
    - Create/Edit a Sales Order:
        - Only products available in the selected warehouse (and the current user) should be displayed. This was done via an api call to server.
        - 'Add Product' button dynamically clone a previous product and add to the view.
        - For the Edit view, data needs to be prepopulated and inventory must be updated when order is saved. For easy implementation, inventory was removed from database and then added with new data.
        - Order value is dynamically calculated whenever product, quantity, or price is changed.


## How to run this application
There is no additional step to run this application. Just download the code and run the project as usual: python manage.py runserver


## Future Improvements
- Toggle left menu
- Add filter and sorting to Warehouses, Products, Categories using list.js or django-filter
- Add more reports such as sales by products/channels
- Increment invoice number with customer name as a prefix
- Allow managing products by batch
- Allow creating a new customer when creating a new sales order
- Allow users to manage their profile
- Allow users to load/receive inventory in each warehouse


## References:
- How to dynamically filter ModelChoice's queryset in a ModelForm? [https://simpleisbetterthancomplex.com/questions/2017/03/22/how-to-dynamically-filter-modelchoices-queryset-in-a-modelform.html]

- Paginating the results of a Django forms POST request [https://stackoverflow.com/a/2266950]

- How to add an event listener to multiple elements in JavaScript [https://flaviocopes.com/how-to-add-event-listener-multiple-elements-javascript/]