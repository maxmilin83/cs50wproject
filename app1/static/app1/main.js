function generatecoins(){

    return fetch(`/generatecoins`)
        .then(response => response.json())
        .then(data => {
            return data;
        })
}



function dataSet(data) {
    const dataSet = data['data'].map(element => {
        let coinPrice = element['quote']['USD']['price'].toFixed(2);
        let coinMarketCap = element['quote']['USD']['market_cap'].toLocaleString('en-US');

        return [
            element['name'], // Name
            `$${coinPrice}`, // Price, formatted as currency
            `$${coinMarketCap}` // Market Cap, formatted as currency
        ];
    });

    // Initialize or update DataTable with dataSet
    $('#table1').DataTable({
        data: dataSet,
        columns: [
            { title: "Name" },
            { title: "Price" },
            { title: "Market Cap" }
        ]
    });
}



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