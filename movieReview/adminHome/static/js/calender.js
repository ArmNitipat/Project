document.addEventListener('DOMContentLoaded', function() {
    var today = new Date();
    var month = String(today.getMonth() + 1).padStart(2, '0'); 
    var year = today.getFullYear(); 

    document.getElementById('monthSelect').value = month;
    document.getElementById('yearSelect').value = year;

    document.getElementById('goButton').addEventListener('click', function() {
        var month = document.getElementById('monthSelect').value;
        var year = document.getElementById('yearSelect').value;

        var url = `/calender/${year}/${month}/`; 

        window.location.href = url;
    });
});
