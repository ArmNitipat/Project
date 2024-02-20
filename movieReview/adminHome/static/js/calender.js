function redirectToScrapingPage() {
    var selectedMonth = document.getElementById("month").value;
    var selectedYear = document.getElementById("year").value;
    var url;
    if (window.location.pathname == '/calender/') {  
        url = "https://www.boxofficemojo.com/calendar/";  
    } else {
        url = "https://www.boxofficemojo.com/calendar/" + selectedYear + "-" + selectedMonth + "-01";
    }
    window.location.href = url;
}