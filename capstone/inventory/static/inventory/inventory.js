document.addEventListener('DOMContentLoaded', function() {
    copy_billing();

    create_order();
})

function create_order() {
    warehouse = document.getElementById('id_warehouse');
    warehouse.addEventListener('change', function() {
        if (warehouse.value !== '') {
            fetch(`/warehouse/${warehouse.value}`)
            .then(response => response.json())
            .then(shelves => {
                // shelves.forEach(load_product)

                // let products = document.getElementById('id_form-0-product');

                const items = document.querySelectorAll('.item .form-select');
                
                items.forEach((item) => {
                    item.innerHTML = '';

                    shelves.forEach((shelf) => {
                        const option = document.createElement("option");
                        option.value = shelf.product_id;
                        option.text = shelf.product + ` [${Math.floor(shelf.quantity)}]`;
                        item.add(option);
                    })
                    
                });
                
                // let quantity = document.getElementById('id_form-0-quantity');
                // let available = document.createElement('div')
                // available.className = 'flex-grow-1 me-3';
                // available.innerHTML = '<div class="form-label">Available</div><input class="form-control" disabled value="1">';
                // quantity.parentNode.parentNode.insertBefore(available, quantity.parentNode);
            })
        }
    })

    add_btn_el = document.getElementById('add_product');
    add_btn_el.addEventListener('click', function() {
        const parent_element = document.getElementById('item-list');
        const copy_origin = document.querySelector('#item-list .item');
        console.log(copy_origin);
        const new_element = copy_origin.cloneNode(true);
        console.log(new_element);
        parent_element.append(new_element);
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