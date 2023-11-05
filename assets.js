// assets.js

document.addEventListener("DOMContentLoaded", function() {
    const assetsButton = document.querySelector(".assets-button");
    const assetsList = document.querySelector(".assets-list");
    
    assetsButton.addEventListener("click", function() {
        // Fetch assets data from the server (API endpoint)
        fetch("/api/assets")
            .then(response => response.json())
            .then(data => {
                // Clear the existing assets
                assetsList.innerHTML = "";
                
                // Populate the assets data in the list
                data.assets.forEach(asset => {
                    const assetElement = document.createElement("div");
                    assetElement.className = "asset";
                    
                    const idElement = document.createElement("div");
                    idElement.className = "id";
                    idElement.textContent = "ID: " + asset.id;
                    assetElement.appendChild(idElement);
                    
                    const macAddressElement = document.createElement("div");
                    macAddressElement.className = "mac-address";
                    macAddressElement.textContent = "MAC Address: " + asset.mac_address;
                    assetElement.appendChild(macAddressElement);
                    
                    const notesElement = document.createElement("div");
                    notesElement.className = "notes";
                    notesElement.textContent = "Notes: " + asset.notes;
                    assetElement.appendChild(notesElement);
                    
                    assetsList.appendChild(assetElement);
                });
            })
            .catch(error => console.log(error));
    });
});
