
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


function dataSet(data) {

        const dataSet = data.map(element => {
            let coinPrice = element['current_price'].toFixed(2);
            let coinMarketCap = element['market_cap'].toLocaleString('en-US');
            let coinName = element['name'];
            let coinId = element['id']
            let coinImage = element['image']
    
            let detailsUrl = `coin/${coinId}`;

            
            return {
                DT_RowAttr: { 'data-href': detailsUrl },
                0: `${coinName} <img src="${coinImage}"; width=22px; >`, 
                1: `$${coinPrice}`, 
                2: `$${coinMarketCap}` 
            };
        });

        $('#table1').DataTable({
            data: dataSet,
            columns: [
                { title: "Name" },
                { title: "Price" },
                { title: "Market Cap" }
            ],
            order: [[2, 'desc']]
        });
}

$('#table1 tbody').on('click', 'tr', function() {
    var href = $(this).data('href');
    if (href) {
        window.location = href;
    }
});


generatecoins().then(response => {
    if(response.data){
        
        dataSet(response.data)
    }else{
        console.log("error");
    }
})



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
    const depositAmount = parseInt(document.querySelector('input[name="amount"]').value || '0');
    let currentMainBalance = parseInt(document.getElementById('main-balance').textContent);
    
    let newBalance = currentMainBalance + depositAmount;
    
    document.getElementById('main-balance').textContent = newBalance;
    document.getElementById('navbar-balance').textContent = '$'+ newBalance+" ";
});

// UPDATE WITHDRAW BALANCE 
document.addEventListener('fundsWithdrew', function() {
    const withdrawAmount = parseInt(document.querySelector('input[name="amount"]').value || '0');
    let currentMainBalance = parseInt(document.getElementById('main-balance').textContent);
    
    let newBalance = currentMainBalance - withdrawAmount;
    
    document.getElementById('main-balance').textContent = newBalance;
    document.getElementById('navbar-balance').textContent = '$'+ newBalance+" ";
});


// form deposit validation

document.body.addEventListener('htmx:beforeRequest', function(event) {
    const form = document.getElementById("modalform");
    const amountinput = form.querySelector('input[name="amount"]').value;
    if (parseInt(amountinput) <= 0) {
        document.getElementById('modal-error').style.display = 'inline';
        event.preventDefault();
    }
    }
);


document.body.addEventListener('htmx:beforeRequest', function(event) {
    const form = document.getElementById("withdrawmodalform");
    const amountinput = form.querySelector('input[name="amount"]').value;
    let mainbal = parseInt(document.getElementById('main-balance').textContent);
    if (parseInt(amountinput) <= 0) {
        document.getElementById('modal-error').innerHTML = 'Must be positive number';
        document.getElementById('modal-error').style.display = 'inline';
        event.preventDefault();
    }else if(parseInt(amountinput) > mainbal){
        document.getElementById('modal-error').innerHTML = 'Cannot withdraw more than current balance';
        document.getElementById('modal-error').style.display = 'inline';
        event.preventDefault();
    }

    }
);