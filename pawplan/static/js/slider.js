// static/slider.js
document.addEventListener("DOMContentLoaded", function() {
    var images = [
        "{% static 'images/dogs/Dog1.png' %}",
        "{% static 'images/dogs/Dog2.png' %}"
    ];
    var currentIndex = 0;
    var slider = document.getElementById("slider");

    function rotateImage() {
        slider.src = images[currentIndex];
        currentIndex = (currentIndex + 1) % images.length;
    }

    setInterval(rotateImage, 3000); // Change image every 3 seconds
});

