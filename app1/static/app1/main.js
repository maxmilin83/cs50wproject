function generatecoins(){

    return fetch(`/generatecoins`)
        .then(response => response.json())
        .then(data => {
            return data;
        })
}



function dataSet(data) {
    console.log("test");
    const dataSet = data['data'].map(element => {
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


generatecoins().then(data => {
    console.log(dataSet(data));

})









// function generatePage(event){

//     let currentpage = document.getElementById("currentpage");

//     if (!event){
//         currentpage.innerHTML = 1;
//     }
//     else{
//         if(event.target.id == 'nextbutton'){
//             currentpage.innerHTML = parseInt(currentpage.innerHTML) + 1
//         }
//         else if(event.target.id == 'previousbutton' && parseInt(currentpage.innerHTML) > 1){
//             currentpage.innerHTML = parseInt(currentpage.innerHTML) - 1
//         }
//     }
//     generatecoins().then(data => {
//         generateTable(data);

//     })
// }







// searchbar.addEventListener("input", () =>{
//     displayData();
// });


// const displayData = async () =>{
//     let table = document.getElementById("table1");
//     let query = searchbar.value;
//     const data = await populateCoinTable();
//     console.log(query);



    // let dataDisplay = data.filter((eventData) => {
    //     if(query === "") {return eventData}
    //     else if(eventData.name.toLowerCase().includes(query.toLowerCase())) {return eventData}
    // }).map((object) => {

    //     const coin = object['name'];
    
    //     return `<p>${coin}</p>              
    //             `
    // }).join("");

    // displaydata.innerHTML = dataDisplay;

// }

// displayData();


// document.addEventListener("DOMContentLoaded", generatePage());

