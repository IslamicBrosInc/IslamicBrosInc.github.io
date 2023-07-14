document.addEventListener('DOMContentLoaded', function() {
    const readMoreElements = document.querySelectorAll('.read-more');
    readMoreElements.forEach(function(element) {
        element.addEventListener('click', function() {
            const cardBody = this.parentNode.parentNode.querySelector('.card-body');
            cardBody.classList.toggle('expanded');
            if (this.innerText === 'Read More') {
                this.innerText = 'Read Less';
            } else {
                this.innerText = 'Read More';
            }
        });
    });
});
    