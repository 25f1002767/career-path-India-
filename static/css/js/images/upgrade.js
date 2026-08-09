// Scroll reveal animation
const revealElements = document.querySelectorAll(".reveal");

function revealOnScroll(){

    revealElements.forEach(el => {

        const top = el.getBoundingClientRect().top;

        if(top < window.innerHeight - 100){

            el.classList.add("active");

        }

    });

}

window.addEventListener("scroll", revealOnScroll);
revealOnScroll();

// Animated counters
document.querySelectorAll(".counter").forEach(counter => {

    const target = +counter.dataset.target;

    let count = 0;

    const update = () => {

        count += Math.ceil(target / 50);

        if(count >= target){

            counter.innerText = target;
            return;
        }

        counter.innerText = count;

        requestAnimationFrame(update);

    };

    update();

});