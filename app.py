from flask import Flask, request, jsonify
import requests

app = Flask(_name_)

TEST_SERVER_API_URL = "http://20.244.56.144/test/register"
ECOMMERCE_API_ENDPOINTS = {
    "Company1": "http://company1.com/api/products",
    "Company2": "http://company2.com/api/products",
    "Company3": "http://company3.com/api/products",
    "Company4": "http://company4.com/api/products",
    "Company5": "http://company5.com/api/products"
}

def register_with_test_server():
    response = requests.post(TEST_SERVER_API_URL)
    if response.status_code == 200:
        print("Successfully registered with Test Server API")
    else:
        print("Failed to register with Test Server API")

def fetch_products(company, category):
   response = requests.get(ECOMMERCE_API_ENDPOINTS[company], params={"category": category})
   if response.status_code == 200:
        return response.json()
   else:
        return []

def sort_products(products, sort_by, sort_order):
    sorted_products = sorted(products, key=lambda x: x.get(sort_by, 0), reverse=(sort_order == "desc"))
    return sorted_products

@app.route('/categories/<categoryname>/products')
def get_top_products(categoryname):
    n = int(request.args.get('n', 10))
    page = int(request.args.get('page', 1))
    sort_by = request.args.get('sort_by', 'rating')
    sort_order = request.args.get('sort_order', 'desc')
    
    products = []
    for company in ECOMMERCE_API_ENDPOINTS:
        company_products = fetch_products(company, categoryname)
        products.extend(company_products)

    sorted_products = sort_products(products, sort_by, sort_order)
    start_index = (page - 1) * n
    end_index = min(start_index + n, len(sorted_products))
    paginated_products = sorted_products[start_index:end_index]

    return jsonify(paginated_products)

@app.route('/categories/<categoryname>/products/<productid>')
def get_product_details(categoryname, productid):
    product_details = {}
    return jsonify(product_details)

if _name_ == '_main_':
    register_with_test_server() 
    app.run(debug=True)  