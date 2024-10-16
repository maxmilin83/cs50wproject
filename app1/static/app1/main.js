
async function generatecoins(){
  
    try{
        const response = await fetch("/generatecoins")
        if(!response.ok){
             return { error: "Failed to fetch data" };
        }
    
        const data = await response.json();
        return data
    }

    catch(error){
        return { error: "Failed to fetch data" };
    }
}

generatecoins().then(response => {
    if(response.data){
        dataSet(response.data)
    }else{
        console.log("error");
    }
})


function dataSet(data) {
        const dataSet = data
                .map(element => {

                let coinPrice = element['current_price'].toFixed(2);
                let coinMarketCap = element['market_cap'].toLocaleString('en-US');
                let coinName = element['name'];
                let coinId = element['id']
                let coinImage = element['image']
                let coinPriceChange = element['price_change_percentage_24h'].toFixed(2)
        
                let detailsUrl = `coin/${coinId}`;
                return {
                    DT_RowAttr: { 'data-href': detailsUrl },
                    0: `${coinName} <img src="${coinImage}"; width=22px; >`, 
                    1: `$${coinPrice}`, 
                    2: `$${coinMarketCap}`,
                    3: `${coinPriceChange}%`
                };
            }
        );

        $('#table1').DataTable({
            data: dataSet,
            columns: [
                { title: "Name" },
                { title: "Price" },
                { title: "Market Cap" },
                { title: "24h Change" }
            ],
            order: [[2, 'desc']],
            responsive: {
                details: {
                    type: 'column',
                    target: ''
                }
            },
            // change color of 24h change text
            createdRow: function(row, data, dataIndex) {
                const changeValue = parseFloat(data[3]);
                if (changeValue > 0) {
                    $('td:eq(3)', row).css('color', '#8cc2ff');
                    $('td:eq(3)', row).css('text-shadow','0 0 12px #8cc2ff');
                } else if (changeValue < 0) {
                    $('td:eq(3)', row).css('color', 'red');
                    $('td:eq(3)', row).css('text-shadow','0 0 2px #ff0000');
                }

            }
        });
}

$('#table1 tbody').on('click', 'tr', function() {
    var href = $(this).data('href');
    if (href) {
        window.location = href;
    }
});







// SHOW MODAL
const modal = new bootstrap.Modal(document.getElementById("modal"))

htmx.on("htmx:afterSwap", (e) => {
  // Response targeting #dialog => show the modal
  if (e.detail.target.id == "dialog") {
    modal.show()
  }
})

// HIDE MODAL

htmx.on("htmx:beforeSwap", (e) => {
    // Empty response targeting #dialog => hide the modal
    if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
      modal.hide()
      e.detail.shouldSwap = false
    }
  })

// flush model errors when exit
htmx.on("hidden.bs.modal", () => {
    document.getElementById("dialog").innerHTML = ""
  })


// UPDATE DEPOSIT BALANCE 

document.addEventListener('fundsAdded', function() {
    const depositAmount = parseFloat(document.querySelector('input[name="amount"]').value || '0');
    
    let currentMainBalance = parseFloat(document.getElementById('main-balance').textContent);
    
    let newBalance = (currentMainBalance + depositAmount).toFixed(2);    
    document.getElementById('main-balance').textContent = newBalance;
    document.getElementById('navbar-balance').textContent = '$'+ newBalance+" ";
});

// UPDATE WITHDRAW BALANCE 
document.addEventListener('fundsWithdrew', function() {
    const withdrawAmount = parseFloat(document.querySelector('input[name="amount"]').value || '0');
    let currentMainBalance = parseFloat(document.getElementById('main-balance').textContent);
    
    let newBalance = (currentMainBalance - withdrawAmount).toFixed(2);
    
    document.getElementById('main-balance').textContent = newBalance;
    document.getElementById('navbar-balance').textContent = '$'+ newBalance+" ";
});


// form deposit validation

document.body.addEventListener('htmx:beforeRequest', function(event) {
    const form = document.getElementById("modalform");
    const amountinput = form.querySelector('input[name="amount"]').value;
    if (parseFloat(amountinput) <= 0) {
        document.getElementById('modal-error').style.display = 'inline';
        event.preventDefault();
    }
    }
);


document.body.addEventListener('htmx:beforeRequest', function(event) {
    const form = document.getElementById("withdrawmodalform");
    const amountinput = form.querySelector('input[name="amount"]').value;
    let mainbal = parseFloat(document.getElementById('main-balance').textContent);
    if (parseFloat(amountinput) <= 0) {
        document.getElementById('modal-error').innerHTML = 'Must be positive number';
        document.getElementById('modal-error').style.display = 'inline';
        event.preventDefault();
    }else if(parseFloat(amountinput) > mainbal){
        document.getElementById('modal-error').innerHTML = 'Cannot withdraw more than current balance';
        document.getElementById('modal-error').style.display = 'inline';
        event.preventDefault();
    }

    }
);

