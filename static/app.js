$("#file").change(function(){
	if ($(this).val().length){
	var f = document.getElementById("file").value
	f = f.replace(/.*[\/\\]/, '')
	document.getElementById("label").innerHTML= "<strong>"+f+"</strong>" 
	   document.getElementsByClassName("danger")[0].classList.add("hide")

	}
})
$("#btn").click(function(){
   if($('#file').val().length){
	var f = document.getElementById("file").value
	f = f.replace(/.*[\/\\]/, '')
	document.getElementById("label").innerHTML=  "<strong>"+f+"</strong>" 
  document.getElementsByClassName("danger")[0].classList.add("hide")
   document.getElementsByClassName("loader")[0].classList.remove("hide")
   }
   else{
	   document.getElementsByClassName("danger")[0].classList.remove("hide")
	   
   }
})