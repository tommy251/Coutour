async function fetchCheapest(category) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "<p>Loading...</p>";  // Show loading state

    try {
        const response = await fetch(`http://localhost:5000/api/cheapest/${category}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        
        if (data.error) {
            resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
        } else {
            resultDiv.innerHTML = `
                <h3>${data.name}</h3>
                <p>Price: NGN ${data.price}</p>
                <a href="${data.url}" target="_blank">View on Jumia</a>
            `;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p>Failed to fetch data: ${error.message}</p>`;
        console.error("Fetch error:", error);
    }
    console.log("Response:", data);
}