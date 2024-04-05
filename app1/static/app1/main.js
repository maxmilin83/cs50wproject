const API_KEY = "CG-LRes7phfWW1qCLTsPaGw5no8"

const searchbar = document.getElementById('searchbar');
const displaydata = document.getElementById('displaydata');


// const getData = async () =>{
//     const res = await fetch(`https://api.coingecko.com/api/v3/coins/list`,{
//         method: 'GET',
//         headers:{
//             'x-cg-demo-api-key': API_KEY
//         }}
//     );

//     if(!res.ok){
//         throw new Error(`HTTP Error status ${res.status}`)
//     }
    
//     const data = await res.json();
//     return data;
// }



const getCoinData = async (pagenum) =>{

    const res = await fetch(`https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=${pagenum}&sparkline=false&locale=en`,{
        method:'GET',
        headers: {'x-cg-demo-api-key': API_KEY},
        });

    data = await res.json();
    return data
}

function generateTable(data){
    let table = document.getElementById("table1");
    $("#table1 tr").detach();
    data.forEach(element => {
        let coinName = element['name']
        let coinPrice = element['current_price']
        let coinMarketCap = element['market_cap']
        coinMarketCap = coinMarketCap.toLocaleString('en-US');
        let coinImage = element['image']
        let newRow = table.insertRow();
        let cell1 = newRow.insertCell(0);
        let cell2 = newRow.insertCell(1);
        let cell3 = newRow.insertCell(2);

        cell1.innerHTML = coinName+" "
        cell1.innerHTML += `<img style="height:15px;" src=${coinImage}>`
        cell2.innerHTML = `$${coinPrice}`
        cell3.innerHTML = `$${coinMarketCap}`
    })
}

function generatePage(event){

    let currentpage = document.getElementById("currentpage");

    if (!event){
        currentpage.innerHTML = 1;
    }
    else{
        if(event.target.id == 'nextbutton'){
            currentpage.innerHTML = parseInt(currentpage.innerHTML) + 1
        }
        else if(event.target.id == 'previousbutton' && parseInt(currentpage.innerHTML) > 1){
            currentpage.innerHTML = parseInt(currentpage.innerHTML) - 1
        }
    }


    getCoinData(currentpage.innerHTML)
        .then(data =>{
            console.log(data);
            generateTable(data);
        })

        .catch(error => {
            console.error('Failed to fetch coin data:', error);
        });
}






searchbar.addEventListener("input", () =>{
    displayData();
});


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


document.addEventListener("DOMContentLoaded", generatePage());