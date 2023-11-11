<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css"></link>
document.addEventListener('DOMContentLoaded', (event) => {
    const stars = document.querySelectorAll('.stars i');
    const ratingInput = document.getElementById('rating');
  
    stars.forEach((star, index) => {
      star.addEventListener('click', () => {
        ratingInput.value = index + 1;  // Set the rating
        highlightStars(index);
      });
  
      star.addEventListener('mouseenter', () => {
        highlightStars(index);
      });
  
      star.addEventListener('mouseleave', () => {
        highlightStars(ratingInput.value - 1);  // Reset to the current rating
      });
    });
  
    function highlightStars(index) {
      stars.forEach((star, idx) => {
        if (idx <= index) {
          star.classList.add('active');
        } else {
          star.classList.remove('active');
        }
      });
    }
  });
