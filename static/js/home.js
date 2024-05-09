if ($(window).width() < 400) {
  $("input[type='text']").attr("placeholder", "Input URL");
  $("input[type='text']").css("font-size", "15px");
} else {
  $("input[type='text']").attr("placeholder", "Input The News URL...");
}

var loadingReal = document.getElementById("loading");
loadingReal.style.display="none";
function loading(){
  $("#loading").show();
  masterhead.style.opacity ="0.7";

  setTimeout(()=>{
    $("#loading").hide();
    masterhead.style.opacity ="1";
  },6000);
}


const masterhead = document.getElementById("masterhead");
const toggle = document.getElementById("toggleDark");
const navbar = document.getElementById("navbar");
const predictbtn = document.getElementById("button-addon2");
const titlehome = document.querySelectorAll("header.masthead h1");
const fontNavbar = document.querySelectorAll("#font-navbar");
const logo = document.getElementById("logo");
toggle.addEventListener("click", function () {
  var theme;
  this.classList.toggle("bi-moon");
  if (this.classList.toggle("bi-brightness-high-fill")) {
    theme = "LIGHT";
  } else {
    theme = "DARK";
  }
  localStorage.setItem("PageTheme", JSON.stringify(theme));
});
setInterval(() => {
  let GetTheme = JSON.parse(localStorage.getItem("PageTheme"));
  if (GetTheme === "DARK") {
    toggle.classList.remove("bi-brightness-high-fill");
    toggle.classList.add("bi-moon");
    titlehome[0].style.color = "#fff";
    predictbtn.style.backgroundColor = "#343A40";
    masterhead.style.background =
      "url('/static/assets/main-bg-dark.webp') no-repeat center center fixed";
    navbar.style.backgroundColor = "#555";
    fontNavbar[0].style.color = "#fff";
    fontNavbar[1].style.color = "#fff";
    fontNavbar[2].style.color = "#fff";
    toggle.style.color = "#fff";
    logo.src = "/static/assets/logodarks.jpeg";
    logo.style.borderRadius = "10px";
  } else {
    masterhead.style.background = toggle.style.color =
      "url('/static/assets/main-bg.jpg') no-repeat center center fixed";
    titlehome[0].style.color = "#606c38";
    navbar.style.backgroundColor = "#f1f3f5";
    predictbtn.style.backgroundColor = "#606c38";
    fontNavbar[0].style.color = "rgba(0,0,0,.55)";
    fontNavbar[1].style.color = "rgba(0,0,0,.55)";
    fontNavbar[2].style.color = "rgba(0,0,0,.55)";
    toggle.style.color = "#000";
    logo.src = "/static/assets/newlogo.png";
  }
}, 5);
