// Click animation
document.addEventListener("click", function(e){

    const burst = document.createElement("div");

    burst.className = "burst";

    burst.style.left = e.clientX + "px";
    burst.style.top  = e.clientY + "px";

    document.body.appendChild(burst);

    setTimeout(() => burst.remove(), 800);

});

// Simple moving particles
const canvas = document.getElementById("particles");
const ctx = canvas.getContext("2d");

let particles = [];

function resize(){

    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;

}

window.addEventListener("resize", resize);
resize();

for(let i=0;i<120;i++){

    particles.push({

        x: Math.random()*canvas.width,
        y: Math.random()*canvas.height,
        r: Math.random()*2 + 1,
        dx:(Math.random()-.5)*0.6,
        dy:(Math.random()-.5)*0.6

    });

}

function animate(){

    ctx.clearRect(0,0,canvas.width,canvas.height);

    particles.forEach(p => {

        p.x += p.dx;
        p.y += p.dy;

        if(p.x<0 || p.x>canvas.width) p.dx *= -1;
        if(p.y<0 || p.y>canvas.height) p.dy *= -1;

        ctx.beginPath();
        ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
        ctx.fillStyle = "rgba(255,255,255,.7)";
        ctx.fill();

    });

    requestAnimationFrame(animate);

}

animate();