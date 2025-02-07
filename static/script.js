function pingBuilding(building) {
    fetch(`/ping/${building}`)
    .then(response => response.json())
    .then(data => {
        Object.keys(data).forEach(host => {
            let status = data[host];
            let circle = document.getElementById(host).querySelector(".circle");

            if (status === "active") {
                circle.className = "circle green";
            } else {
                circle.className = "circle red";
            }
        });
    })
    .catch(error => console.error("Error pinging:", error));
}
