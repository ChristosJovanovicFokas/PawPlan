let slider = document.querySelector('.slider');
let slides = document.querySelectorAll('.slide');
let slideIndex = 0;

function nextSlide() {
    slideIndex++;
    if (slideIndex === slides.length) {
        slideIndex = 0;
    }
    updateSlidePosition();
}

function updateSlidePosition() {
    let offset = -slideIndex * slides[0].offsetWidth;
    slider.style.transform = `translateX(${offset}px)`;
}

// Auto-advance slides every 3 seconds
setInterval(nextSlide, 3000);
