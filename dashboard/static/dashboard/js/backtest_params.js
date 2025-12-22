
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".clickable-row").forEach(row => {
        row.addEventListener("click", () => {
            window.location = row.dataset.href;
        });
    });
});


// document.addEventListener("DOMContentLoaded", function(){
//     const strategySelect = document.getElementById("strategy-select");
//     const emaParam = document.getElementById("ema-param-container");
//     const rsiParam = document.getElementById("rsi-param-container");
//     const bbParam = document.getElementById("bb-param-container");


//     strategySelect.addEventListener("change", function(){

//             let selected = strategySelect.options[strategySelect.selectedIndex];
//             let schema = selected.getAttribute("data-schema");
//             console.log(schema);
//             if (schema == "EMA Crossover"){
//                 emaParam.style.display = "block";
//                 rsiParam.style.display = "none";
//                 bbParam.style.display = "none";
//             } else if(schema == "RSI Mean Reversion"){
//                 rsiParam.style.display = "block";
//                 emaParam.style.display = "none";
//                 bbParam.style.display = "none";
//             } else if(schema == "Bollinger Bands"){
//                 bbParam.style.display = "block";
//                 rsiParam.style.display = "none";
//                 emaParam.style.display = "none";
//             }
            
           



//     })
//     document.querySelector("form").addEventListener("submit", function (event) {
//         const inputs = paramContainer.querySelectorAll("input");
//         let paramDict = {};

//         inputs.forEach(input => {
//             let value = input.value;
//             if (value === "") {
//                 value = null;
//             } else if (!isNaN(value)) {
//                 value = Number(value);
//             }
//             paramDict[input.name] = value;
//         });

//         hiddenJsonField.value = JSON.stringify(paramDict);
//     });
// })
