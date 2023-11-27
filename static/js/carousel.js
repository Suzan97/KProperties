// To make the slide move after 15 seconds

(function() {
  var slides = document.querySelectorAll('.aa-top-slider-single');
  var currentSlide = 0;

  setInterval(() => {
    currentSlide = (currentSlide + 1) % slides.length;

    slides.forEach((slide, index) => {
      slide.style.display = index === currentSlide ? 'block' : 'none';
    });
  }, 15000);
})();
