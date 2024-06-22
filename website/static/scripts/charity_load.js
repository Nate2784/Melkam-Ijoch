document.addEventListener("DOMContentLoaded", function () {
    const loadMoreButton = document.getElementById("load-more-btn");
    const charityCards = document.querySelectorAll(".charity-card");
    const initialCharityCount = 3; // Show 6 initially
    let visibleCharityCount = initialCharityCount;

    // Hide extra charity cards initially
    for (let i = initialCharityCount; i < charityCards.length; i++) {
        charityCards[i].style.display = "none";
    }

    loadMoreButton.addEventListener("click", () => {
        for (let i = visibleCharityCount; i < visibleCharityCount + initialCharityCount; i++) {
            if (charityCards[i]) {
                charityCards[i].style.display = "block";
            }
        }
        visibleCharityCount += initialCharityCount;

        // Hide button when all charities are visible
        if (visibleCharityCount >= charityCards.length) {
            loadMoreButton.style.display = "none";
        }
    });
});
