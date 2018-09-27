

var forusConfig = JSON.parse(document.getElementById('forus_params').text)


var forus_div = document.getElementById('forus_button')

forus_div.innerHTML = "<div id='forus_popup'></div><div id='forus_login_button' style='cursor:pointer;padding: 15px;background-color:blue;color:white;font-family:sans-serif;text-transform:uppercase;display:inline-block;'> Forus login identity</div>"

var button = document.getElementById("forus_login_button");
button.addEventListener("click", function(){
    var data = {
      public_key: forusConfig.FORUS_API_KEY,
    };

    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    xmlhttp.open('POST', "/en/organisation/create_login/?format=json", true);
    xmlhttp.setRequestHeader("Content-Type", "application/json");
    xmlhttp.onreadystatechange = function() {
      if (this.readyState != 4) return;

      token = JSON.parse(this.responseText).token;
      showToken(token)
    }
    xmlhttp.send(JSON.stringify(data));


}, false);


function showToken(token){
    var forus_popup = document.getElementById('forus_popup')

    forus_popup.innerHTML = "<div id='forus_popup_wrapper' style='display:flex;position:fixed;top:0;right:0;bottom:0;left:0;justify-content:center;align-items:center;background-color:rgba(0,0,0,.2);'>" +
            "<div style='background-color:#fff;padding:20px;position:relative'>" +
                "<div id='forus_popup_close' style='display:flex;justify-content:center;align-items:center;background:#fff;border-radius:15px;width:30px;height:30px;position:absolute;top:-40px;right:0px;cursor:pointer'><img style='width:15px' src='https://freeiconshop.com/wp-content/uploads/edd/cross-solid.png'/></div>" +
                "<img src='" + "/en/organisation/qr/?text=" +  token +  "' style='max-width: 300px;' />"+
            "</div>"+
        "</div>";

    var closeButton = document.getElementById('forus_popup_close');
    var popupWrapper = document.getElementById('forus_popup_wrapper');

    closeButton.addEventListener("click", function(){
        popupWrapper.style.display = 'none';
    });

    window.setInterval(function(){
        check_login()
    }, 1000);

}

function check_login() {

}

//data.FORUS_API_KEY

