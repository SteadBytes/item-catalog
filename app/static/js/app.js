var clicked = false;

function onClick() {
	clicked = true;
	document.getElementById("gsignin").src = "/static/images/gsignin_pressed.png";
}

function onMouseOver() {
	if (!clicked)
		document.getElementById("gsignin").src = "/static/images/gsignin_focus.png";
}

function onMouseOut(obj) {
	if (!clicked)
		obj.src = "/static/images/gsignin.png";
}
