
var host = "http://136.144.185.49/"

var forusConfig = JSON.parse(document.getElementById('forus_params').text)

var ibmPlexStyle = document.createElement('link');
ibmPlexStyle.rel = 'stylesheet';
ibmPlexStyle.href = 'https://fonts.googleapis.com/css?family=IBM+Plex+Sans';
document.getElementsByTagName('head')[0].appendChild(ibmPlexStyle);

var forus_div = document.getElementById('forus_button')

forus_div.innerHTML = "<div id='forus_popup'></div><div id='forus_login_button' style='cursor:pointer;padding: 15px;background-color:blue;color:white;font-family:sans-serif;text-transform:uppercase;display:inline-block;'> Forus login identity</div>"
var button = document.getElementById("forus_login_button");
button.addEventListener("click", function(){
    var data = {
      public_key: forusConfig.FORUS_API_KEY,
    };

    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    xmlhttp.open('POST', host + "en/organisation/create_login/?format=json", true);
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

    forus_popup.innerHTML = "<div id='forus_popup_wrapper' style='display:flex;position:fixed;top:0;right:0;bottom:0;left:0;justify-content:center;align-items:center;background-color:rgba(0,0,0,.2)'>" +
        "<div style='background-color:#fff;padding:20px;position:relative; max-width: 340px; text-align: center; font-family: \"IBM Plex Sans\", sans-serif; font-size: 16px'>"
        + '<div style="text-align: left">'
        + '<p>Bedankt voor je interesse, om je stem mee te laten tellen dien je aan te tonen dat je:</p>'
        + '<ul style="list-style: none; padding: 0">'
        + '<li>&mdash; Woont in Angelslo</li>'
        + '<li>&mdash; Ouder bent dan 18</li>'
        + '</ul>'
        + '</div>'
        + '<div style="display: inline-block; width: 300px; text-align: left">'
        + '<p style="display: block; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; color: #0f55f0">Bevestig met:</p>'
        + '<select name="provider" style="display: block; color: #0f55f0; width: 100%; height: 50px; line-height: 46px; border: 2px solid #d9dee2; border-radius: 2px; font-size: 18px; padding-left: 15px; background-color: #f3f3f3">'
        + '<option value="me">Me</option>'
        + '<option value="irma">IRMA</option>'
        + '<option value="digid">DigiD</option>'
        + '<option value="idin">IDIN</option>'
        + '<option value="uport">uPort</option>'
        + '</select>'
        + '</div>'
    +           "<img src='" + host + "en/organisation/qr/?text=" +  token +  "' style='max-width: 300px; display: inline-block' />"
    +
    
                "<div id='forus_popup_close' style='display:flex;justify-content:center;align-items:center;background:#fff;border-radius:15px;width:30px;height:30px;position:absolute;top:-40px;right:0px;cursor:pointer'><img style='width:15px' src='https://freeiconshop.com/wp-content/uploads/edd/cross-solid.png'/></div>" +
      
            "</div>"+
        "</div>";

    var closeButton = document.getElementById('forus_popup_close');
    var popupWrapper = document.getElementById('forus_popup_wrapper');

    closeButton.addEventListener("click", function(){
        popupWrapper.style.display = 'none';
    });

    window.setInterval(function(){
        check_login(token)
    }, 1000);

}


var lastStatus = ''
function check_login(token) {


    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
    xmlhttp.open('GET', host + "en/organisation/login/info/?key="+token, true);
    xmlhttp.setRequestHeader("Content-Type", "application/json");
    xmlhttp.onreadystatechange = function() {
        if (this.readyState != 4) return;

        result = JSON.parse(this.responseText)
        if (result.status != 'new') {
            if (lastStatus != result.status) {
                lastStatus = result.status
                alert(result.status)
            }
        }

    }
    xmlhttp.send(JSON.stringify({}));
}

//data.FORUS_API_KEY

