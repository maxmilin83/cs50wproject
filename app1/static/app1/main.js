// function generatecoins(){

//     return fetch(`/generatecoins`)
//         .then(response => response.json())
//         .then(data => {
//             console.log(data);
//             // return data;
//         })
        

// }

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



