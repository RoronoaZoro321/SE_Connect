document.addEventListener("DOMContentLoaded", function () {
    const fireworkContainer = document.getElementById("fireworkContainer");

    function createFirework() {
        const firework = document.createElement("div");
        firework.className = "firework";
        firework.style.left = Math.random() * 100 + "vw";
        firework.style.top = Math.random() * 100 + "vh";
        firework.style.backgroundColor = getRandomColor();

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

    setInterval(createFirework, 200);
    setInterval(createFirework, 200);

});
