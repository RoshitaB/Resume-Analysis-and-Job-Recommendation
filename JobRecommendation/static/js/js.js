let input = document.querySelector("input");
let file = document.querySelector(".file");
let fileName = document.querySelector(".fileName");


function changeBackGround() {
  file.style.backgroundColor = "#4ca2cd";
}

function normalizeBackGround() {
  file.style.backgroundColor = "#fff";
}
file.ondragenter = changeBackGround;
file.onfocus = changeBackGround;
file.onclick = changeBackGround;
file.ondragleave = normalizeBackGround;
file.ondrop = normalizeBackGround;
file.onblur = normalizeBackGround;
file.dragend = normalizeBackGround;
file.ondrag = normalizeBackGround;
file.onhover = normalizeBackGround;

input.onchange = function() {
  file.style.backgroundColor = "#fff";
  let displayName = input.value.split("\\").pop().slice(0, 11);
  fileName.textContent = displayName;
}
if(fileName.textContent===""){
	file.style.backgroundColor = "#fff";
}