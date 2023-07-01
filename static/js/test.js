$(document).ready(function() {
  $('#myForm').submit(function(event) {
    console.log('Form submitted');
    // Prevent the default form submission
    event.preventDefault();

    // Create a new FormData object
    var formData = new FormData();

    // Append the file data to the form data object
    formData.append('fileup', $('#entry_value')[0].files[0]);

    // Send the form data to the server using AJAX
    $.ajax({
      type: 'POST',
      url: '/predict', // Replace with the URL of your Flask route
      data: formData,
      contentType: false,
      processData: false,
      success: function(response) {
        // Extract the prediction result from the JSON response
        var prediction = response.prediction;
document.getElementById('prediction').innerText = prediction;
        // Display the prediction result in the #response55 div
        $('#response55').html(prediction);
      }
    });
  });
});


let imagecon = document.getElementById("image_view")
let result = document.querySelector(".result p")
let infile = document.getElementById("entry_value")

/*uploadImage*/
infile.addEventListener("change", function(){
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.addEventListener("load",function(){
            imagecon.style.display = "block";
            imagecon.setAttribute("src", this.result);
        })
        reader.readAsDataURL(file)
    }
})

/*add result*/
check.onclick = function() {
    var cartonna = "";
    for (var i = 1; i < 2; i++) {
        cartonna += `<tr>
        <td class="kill">${i}</td>
        <td class="kill"><img src="" alt="" style="width: 40px; "></td>
        <td class="kill" id="prediction"></td>
        <td class="kill"> <button class="btn btn-outline-danger" id="delee" onclick="deleteRow()" >delete</button></td>
        </tr>`

    };
    document.getElementById("TableBody").innerHTML = cartonna;

    // Wait for the image to load before inserting it into the table
    imagecon.onload = function() {
        document.querySelector("#TableBody img").setAttribute("src", imagecon.src);
    };

    document.getElementById("delee").onclick = function() {
        document.getElementById("TableBody").innerHTML = "";
        document.getElementById("image_view").style.display = "none";
    }
}
function image_test(){
    document.getElementById('image_test_parkinson').style.display="block"
    
    document.getElementById('voice_test_parkinson').style.display="none"
}

function voice_test(){
    document.getElementById('image_test_parkinson').style.display="none"
    
    document.getElementById('voice_test_parkinson').style.display="block"
}




