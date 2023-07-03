



const slidePage = document.querySelector(".slide-page");
const nextBtnFirst = document.querySelector(".firstNext");
const prevBtnSec = document.querySelector(".prev-1");
const nextBtnSec = document.querySelector(".next-1");
const prevBtnThird = document.querySelector(".prev-2");
const nextBtnThird = document.querySelector(".next-2");
const prevBtnFourth = document.querySelector(".prev-3");
const submitBtn = document.querySelector(".submit");
const progressText = document.querySelectorAll(".step p");
const progressCheck = document.querySelectorAll(".step .check");
const bullet = document.querySelectorAll(".step .bullet");
let current = 1;

function checkInputs(step) {
  const inputs = step.querySelectorAll('input[required], select[required]');
  let isValid = true;
  for (let i = 0; i < inputs.length; i++) {
    if (!inputs[i].value) {
      isValid = false;
      const error = document.createElement('div');
      error.classList.add('error');
      error.innerText = '*';

      inputs[i].parentElement.appendChild(error);
    } else {
      const error = inputs[i].parentElement.querySelector('.error');
      if (error) {
        error.remove();
      }
    }
  }
  return isValid;
}

nextBtnFirst.addEventListener("click", function(event){
  event.preventDefault();
  if (checkInputs(slidePage)) {
    slidePage.style.marginLeft = "-25%";
    bullet[current - 1].classList.add("active");
    progressCheck[current - 1].classList.add("active");
    progressText[current - 1].classList.add("active");
    current += 1;
  }
});

nextBtnSec.addEventListener("click", function(event){
  event.preventDefault();
  if (checkInputs(slidePage)) {
    slidePage.style.marginLeft = "-50%";
    bullet[current - 1].classList.add("active");
    progressCheck[current - 1].classList.add("active");
    progressText[current - 1].classList.add("active");
    current += 1;
  }
});

nextBtnThird.addEventListener("click", function(event){
  event.preventDefault();
  if (checkInputs(slidePage)) {
    slidePage.style.marginLeft = "-75%";
    bullet[current - 1].classList.add("active");
    progressCheck[current - 1].classList.add("active");
    progressText[current - 1].classList.add("active");
    current += 1;
  }
});

submitBtn.addEventListener("click", function(){
  if (checkInputs(slidePage)) {
    bullet[current - 1].classList.add("active");
    progressCheck[current - 1].classList.add("active");
    progressText[current - 1].classList.add("active");
    current += 1;
    setTimeout(function(){
      alert("Your Form falied Signed up");
      location.reload();
    },800);
  }
});

prevBtnSec.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "0%";
  bullet[current - 2].classList.remove("active");
  progressCheck[current - 2].classList.remove("active");
  progressText[current - 2].classList.remove("active");
  current -= 1;
});

prevBtnThird.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "-25%";
  bullet[current - 2].classList.remove("active");
  progressCheck[current - 2].classList.remove("active");
  progressText[current - 2].classList.remove("active");
  current -= 1;
});

prevBtnFourth.addEventListener("click", function(event){
  event.preventDefault();
  slidePage.style.marginLeft = "-50%";
  bullet[current - 2].classList.remove("active");
  progressCheck[current - 2].classList.remove("active");
  progressText[current - 2].classList.remove("active");
  current -= 1;
});
function clicking(){

document.getElementById("signup").style.display="block"
document.getElementById("signin").style.display="none"
document.getElementById("container-about").style.display="none"

}

function clicking_close(){

document.getElementById("signup").style.display="none"
document.getElementById("signin").style.display="none"
document.getElementById("container-about").style.display="block"


}

function clicking_signin(){

document.getElementById("signin").style.display="block"

document.getElementById("signup").style.display="none"
document.getElementById("container-about").style.display="none"

}
function btn_del(count) {
    var row = document.getElementById('row-' + count);
    row.parentNode.removeChild(row);
}
function clicking_close_in(){

    document.getElementById("signin").style.display="none"
document.getElementById("signup").style.display="none"
document.getElementById("container-about").style.display="block"

}


setTimeout(function() {
  var alert = document.getElementById("my-alert");
   alert.style.opacity = 0;

}, 5000);