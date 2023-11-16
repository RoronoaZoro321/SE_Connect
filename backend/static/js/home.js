document.addEventListener("DOMContentLoaded", function () {
    const fireworkContainer = document.getElementById("fireworkContainer");

    function createFirework(x, y, size, color) {
        const firework = document.createElement("div");
        firework.className = "firework";
        firework.style.left = x + "px";
        firework.style.top = y + "px";
        firework.style.width = size + "px";
        firework.style.height = size + "px";
        firework.style.backgroundColor = color;

        fireworkContainer.appendChild(firework);

        firework.addEventListener("animationend", function () {
            firework.remove();
        });
    }

    function getRandomColor() {
        const letters = "0123456789ABCDEF";
        let color = "#";
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    function handleMouseClick(event) {
        const x = event.clientX;
        const y = event.clientY;
        const size = 70;
        const color = getRandomColor();

        createFirework(x, y, size, color);
    }

    document.addEventListener("click", handleMouseClick);

    setInterval(function () {
        createFirework(
            Math.random() * window.innerWidth,
            Math.random() * window.innerHeight,
            Math.random() * 20 + 5,
            getRandomColor()
        );
    }, 200);
});
