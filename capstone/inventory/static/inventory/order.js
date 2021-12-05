document.addEventListener('DOMContentLoaded', function() {

    // Reload page when 'Reset' is clicked
    document.getElementById('reset').addEventListener('click', () => {
        location.reload();
    })

    // Show all orders including closed ones when 'Show All' is clicked
    document.getElementById('show_all').addEventListener('click', () => {
        alert("HOHO");

        fetch('/order/api')
        .then(response => response.json())
        .then(orders => {
            console.log(orders);
        })
    })
})