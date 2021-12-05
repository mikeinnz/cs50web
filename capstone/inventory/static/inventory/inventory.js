document.addEventListener('DOMContentLoaded', function() {
    // copy billing details over to shipping fields
    copy_billing();

    // dynamically populate products, add a new product and calculate order value when creating a sales order
    create_order();

    // prepopulate order value
    update_order_value();

    // format quantity, price and discount
    format_numbers();
})

function create_order() {
    // populate available products in the selected warehouse
    populate_products();

    // add product
    add_product();
    
    // calculate order value
    calculate_order_value();
}


function populate_products() {
    warehouse = document.getElementById('id_warehouse');
    warehouse.addEventListener('change', function() {
        if (warehouse.value !== '') {
            // reset order value
            document.getElementById('value').innerHTML = 0;

            fetch(`/warehouse/${warehouse.value}`)
            .then(response => response.json())
            .then(shelves => {

                // obtain all dropdown lists
                const items = document.querySelectorAll('.item .form-select');
                
                // set each dropdown list with new options
                items.forEach((item) => {
                    // clear all options
                    item.innerHTML = '';
                    
                    // add no select option
                    const noselect = document.createElement('option');
                    noselect.value = '';
                    noselect.text = '---------';
                    item.add(noselect);

                    // add all available options
                    shelves.forEach((shelf) => {
                        const option = document.createElement('option');
                        option.value = shelf.product_id;
                        option.text = shelf.product + ` [${Math.floor(shelf.quantity)}]`;
                        item.add(option);
                    })
                });
                
            })
        }
    })
}


function add_product() {
    add_btn_el = document.getElementById('add_product');
    const total_items_element = document.getElementById('id_form-TOTAL_FORMS');

    add_btn_el.addEventListener('click', function() {
        const parent_element = document.getElementById('item-list');
        // identify the last item
        const copy_origin = document.querySelector('.item:last-child');
        console.log(copy_origin);

        // copy the last item
        const new_element = copy_origin.cloneNode(true);
        console.log(new_element);
        let total_items = total_items_element.value;

        // replace id with an incremental one
        const regex = new RegExp(`-${total_items - 1}-`, 'g');
        new_element.innerHTML = new_element.innerHTML.replace(regex, `-${total_items}-`);
        parent_element.append(new_element);

        // update form-TOTAL_FORMS with a new number
        total_items_element.value = parseInt(total_items_element.value) + 1;

        // add event listener to this new item as well
        calculate_order_value();

        // format the new added numbers too
        format_numbers();
    })
}

function calculate_order_value() {
    // listen to each change in item details
    document.querySelectorAll('.value').forEach(item => {
        // user a named function instead of arrow function in order to save memory
        item.addEventListener('change', update_order_value);
    })
}

function update_order_value() {
        const total_items = document.getElementById('id_form-TOTAL_FORMS').value;

        // initiate order value
        var value = 0;

        for (let i = 0; i < total_items; i++) {
            product = document.getElementById(`id_form-${i}-product`);

            // only proceed if a valid product is selected
            if (product.value !== '') {
                const quantity = document.getElementById(`id_form-${i}-quantity`).value;
                const price = document.getElementById(`id_form-${i}-price`).value;
                const discount = document.getElementById(`id_form-${i}-discount`).value;
                const sub_total = quantity * (1 - discount) * price;
                value += sub_total;
            }
        }

        // update order value, show up to two decimal places
        document.getElementById('value').innerHTML = new Intl.NumberFormat().format(value.toFixed(2));
}


function format_numbers(){
    // select all input fields for quantity, price, and discount
    document.querySelectorAll(('input.value')).forEach(e => {
        if (parseFloat(e.value) % 1 != 0) {
            // show only two decimal points
            e.value = parseFloat(e.value).toFixed(2);
        }
        else {
            // show whole number
            e.value = parseFloat(e.value).toFixed(0);
        }
    })
}

function copy_billing() {
    copy_billing_btn = document.getElementById('copy_billing')
    if (copy_billing_btn != null) {
        copy_billing_btn.addEventListener('click', function() {
            document.getElementById('id_shipping_street').value = document.getElementById('id_billing_street').value;
            document.getElementById('id_shipping_suburb').value = document.getElementById('id_billing_suburb').value;
            document.getElementById('id_shipping_city').value = document.getElementById('id_billing_city').value;
            document.getElementById('id_shipping_postcode').value = document.getElementById('id_billing_postcode').value;
            document.getElementById('id_shipping_country').value = document.getElementById('id_billing_country').value;
        })
    }
}