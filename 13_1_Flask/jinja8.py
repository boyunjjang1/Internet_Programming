from flask import Flask, render_template

app = Flask(__name__)

someobj = {
    # jsondata.json  파일 내용을 가져올 것
"customer_list": [
        { 
            "CustomerID": 1,
            "CustomerName": "Alfreds Futterkiste",
            "ContactName": "Maria Anders", 
            "Address": "Obere Str. 57", 
            "City": "Berlin", 
            "PostalCode": "12209",
            "Country": "Germany"
        },
        { 
            "CustomerID": 2,
            "CustomerName": "Ana Trujillo Emparedados y helados",
            "ContactName": "Ana Trujillo", 
            "Address": "Avda. de la Constitución 2222", 
            "City": "México D.F.", 
            "PostalCode": "05021",
            "Country": "Mexico"
        },
        { 
            "CustomerID": 3,
            "CustomerName": "Antonio Moreno Taquería",
            "ContactName": "Antonio Moreno", 
            "Address": "Mataderos 2312", 
            "City": "México D.F.", 
            "PostalCode": "05023",
            "Country": "Mexico"
        },
        { 
            "CustomerID": 4,
            "CustomerName": "Around the Horn",
            "ContactName": "Thomas Hardy", 
            "Address": "120 Hanover Sq.", 
            "City": "London", 
            "PostalCode": "WA1 1DP",
            "Country": "UK"
        },
        { 
            "CustomerID": 5,
            "CustomerName": "Berglunds snabbköp",
            "ContactName": "Christina Berglund", 
            "Address": "Berguvsvägen 8", 
            "City": "Luleå", 
            "PostalCode": "S-958 22",
            "Country": "Sweden"
        }
    ]

}

@app.route('/customer')
def index():
    return render_template('customer_list.html', obj=someobj)

@app.route('/customer/<int:customerid>/profile')
def customer_profile(customerid=None):
    customer2 = None
    for customer in someobj['customer_list']:
        if(customer['CustomerID'] == customerid):
            customer2 = customer
            break
    
    if customer2:
        return render_template('customer_profile.html', customer=customer2)
    
    else:
        return 'no customers found'


    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)