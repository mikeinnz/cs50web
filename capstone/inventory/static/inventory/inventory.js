document.addEventListener('DOMContentLoaded', function() {
    copy_billing_btn = document.getElementById('copy_billing')

    copy_billing_btn.addEventListener('click', function() {
        document.getElementById('id_shipping_street').value = document.getElementById('id_billing_street').value;
        document.getElementById('id_shipping_suburb').value = document.getElementById('id_billing_suburb').value;
        document.getElementById('id_shipping_city').value = document.getElementById('id_billing_city').value;
        document.getElementById('id_shipping_postcode').value = document.getElementById('id_billing_postcode').value;
        document.getElementById('id_shipping_country').value = document.getElementById('id_billing_country').value;
    })
})