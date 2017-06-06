var clicked = false;

function onClick() {
	clicked = true;
	document.getElementById("gsignin").src = "/static/images/gsignin_pressed.svg";
}

function onMouseOver() {
	if (!clicked)
		document.getElementById("gsignin").src = "/static/images/gsignin_focus.svg";
}

function onMouseOut(obj) {
	if (!clicked)
		obj.src = "/static/images/gsignin.svg";
}
