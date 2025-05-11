const faqQuestions = document.querySelectorAll('.faq-question');
        
faqQuestions.forEach(question => {
    question.addEventListener('click', () => {
        const answer = question.nextElementSibling;
        const icon = question.querySelector('i');
        
        // Toggle visibility
        if (answer.style.display === 'block') {
            answer.style.display = 'none';
            icon.classList.remove('fa-chevron-up');
            icon.classList.add('fa-chevron-down');
        } else {
            answer.style.display = 'block';
            icon.classList.remove('fa-chevron-down');
            icon.classList.add('fa-chevron-up');
        }
    });
});        

// Initialize FAQ answers as hidden
document.querySelectorAll('.faq-answer').forEach(answer => {
    answer.style.display = 'none';
});

// Form submission handler
document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // You would add actual form submission logic here
    // For now, just show a success message
    alert('Thank you for your message! We will get back to you soon.');
    this.reset();
});        