
$(document).ready(function(){
    var fang = ["FB", "AMZN", "AAPL", "NFLX", "GOOGL"]
    for( var i =0; i<5; i++){
    console.log(fang[i])
    $.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol="+fang[i]+"&apikey=4Z915SHVXI6MZ0PP", function(data_now){
        console.log(data_now)
        var symbol = data_now["Global Quote"]["01. symbol"]
        var price = data_now["Global Quote"]["05. price"]
        // console.log(symbol)
        $(".fang-data").append(function(){
        var name = "<h1>"+symbol+"</h1>"
        var quote = "<p>"+price+"</p>"
        console.log(quote)
        return[name, quote] ;
        })
    })
    }

})
