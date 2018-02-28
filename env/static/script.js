window.onload = function() {
  document.getElementById("itemNameField").focus();

  document.getElementById("itemNameField").addEventListener("keydown", function (e) {
    if (e.keyCode === 13) {
        submit();
    }
  });
};

function submit() {
	alert("hi");
}
