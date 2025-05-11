const burger = document.querySelector('.burger');
const navLinks = document.querySelector('.nav-links');

burger.addEventListener('click', () => {
    navLinks.classList.toggle('nav-active');
    burger.classList.toggle('toggle');
});

// Simple slider functionality
const slides = document.querySelectorAll('.slide');
const indicators = document.querySelectorAll('.indicator');
let currentSlide = 0;

function showSlide(n) {
    slides.forEach(slide => slide.classList.remove('active'));
    indicators.forEach(indicator => indicator.classList.remove('active'));
    
    slides[n].classList.add('active');
    indicators[n].classList.add('active');
    currentSlide = n;
}

// Auto-rotate slides every 5 seconds
setInterval(() => {
    let next = currentSlide + 1;
    if (next >= slides.length) next = 0;
    showSlide(next);
}, 5000);

// Add click event to indicators
indicators.forEach((indicator, index) => {
    indicator.addEventListener('click', () => {
        showSlide(index);
    });
});


document.getElementById("searchBtn").addEventListener("click", function () {
    const input = document.getElementById("searchInput").value.toLowerCase();
    const books = document.querySelectorAll(".book-item");

    books.forEach(book => {
        const title = book.querySelector("h3").textContent.toLowerCase();
        if (title.includes(input)) {
            book.style.display = "block";
        } else {
            book.style.display = "none";
        }
    });
});

// Optional: Pressing Enter triggers search
document.getElementById("searchInput").addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
        document.getElementById("searchBtn").click();
    }
});
