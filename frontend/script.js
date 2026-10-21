const API_URL = "http://127.0.0.1:8000";


// =====================================================
// ELEMENTS
// =====================================================

const selfieInput = document.getElementById("selfieInput");
const fileName = document.getElementById("fileName");
const searchButton = document.getElementById("searchButton");

const loadingSection =
    document.getElementById("loadingSection");

const resultsSection =
    document.getElementById("resultsSection");

const memoryGrid =
    document.getElementById("memoryGrid");

const resultCount =
    document.getElementById("resultCount");

const heroSection =
    document.querySelector(".hero");

const aboutSection =
    document.getElementById("aboutSection");

const navItems =
    document.querySelectorAll(".nav-item");

const logo =
    document.getElementById("logo");


let selectedFile = null;


// =====================================================
// SELECT SELFIE
// =====================================================

selfieInput.addEventListener("change", function () {

    selectedFile = this.files[0];

    if (selectedFile) {

        fileName.textContent =
            `Selected: ${selectedFile.name}`;

    }

});


// =====================================================
// FIND MY MEMORIES
// =====================================================

searchButton.addEventListener("click", async function () {

    // Check selfie
    if (!selectedFile) {

        alert("Please select a selfie first.");

        return;

    }


    // Hide other sections
    heroSection.style.display = "none";

    aboutSection.style.display = "none";

    resultsSection.style.display = "none";


    // Show AI loading
    loadingSection.style.display = "block";


    // Create form data
    const formData = new FormData();

    formData.append(
        "file",
        selectedFile
    );


    try {

        console.log("🔍 Sending selfie to backend...");


        const response = await fetch(
            `${API_URL}/find-memories`,
            {
                method: "POST",
                body: formData
            }
        );


        console.log(
            "Backend response:",
            response.status
        );


        const data = await response.json();


        console.log(
            "AI result:",
            data
        );


        // Backend error
        if (!response.ok || data.error) {

            throw new Error(
                data.error ||
                data.message ||
                "Something went wrong"
            );

        }


        // Display results
        displayMemories(
            data.memories || []
        );


    } catch (error) {

        console.error(
            "❌ Error:",
            error
        );


        loadingSection.style.display =
            "none";


        heroSection.style.display =
            "flex";


        alert(
            "Could not find your memories.\n\n" +
            error.message
        );

    }

});


// =====================================================
// DISPLAY MEMORIES
// =====================================================

function displayMemories(memories) {

    loadingSection.style.display =
        "none";


    resultsSection.style.display =
        "block";


    resultCount.textContent =
        `${memories.length} memories found`;


    memoryGrid.innerHTML = "";


    if (memories.length === 0) {

        memoryGrid.innerHTML = `

            <div class="no-results">

                <div class="no-results-icon">
                    📷
                </div>

                <h3>
                    No matching memories found
                </h3>

                <p>
                    Try uploading another clear selfie.
                </p>

            </div>

        `;

        return;

    }


    memories.forEach((memory, index) => {

        const imageURL =
            `${API_URL}${memory.photo_url}`;


        const matchPercentage =
            (memory.similarity * 100).toFixed(1);


        const card =
            document.createElement("div");


        card.className =
            "memory-card";


        card.innerHTML = `

            <div class="image-container">

                <img
                    src="${imageURL}"
                    alt="Wari Memory"
                >

                <div class="match-badge">
                    ${matchPercentage}% Match
                </div>

            </div>


            <div class="memory-info">

                <span class="memory-number">
                    MEMORY ${index + 1}
                </span>

                <h3>
                    A Moment from Wari
                </h3>

                <div class="memory-details">

                    <p>
                        📍 Pandharpur Wari
                    </p>

                    <p>
                        📅 Wari 2026
                    </p>

                </div>


                <div class="memory-actions">

                    <a
                        href="${imageURL}"
                        download
                        class="download-button">

                        ⬇ Download

                    </a>

                </div>

            </div>

        `;


        memoryGrid.appendChild(card);

    });

}


// =====================================================
// NAVBAR
// =====================================================

navItems.forEach(item => {

    item.addEventListener("click", function () {

        const section =
            this.dataset.section;


        // Active navbar
        navItems.forEach(nav => {

            nav.classList.remove("active");

        });


        this.classList.add("active");


        // -------------------------
        // HOME
        // -------------------------

        if (section === "home") {

            heroSection.style.display =
                "flex";

            aboutSection.style.display =
                "none";

            loadingSection.style.display =
                "none";

            resultsSection.style.display =
                "none";

        }


        // -------------------------
        // ABOUT
        // -------------------------

        else if (section === "about") {

            heroSection.style.display =
                "none";

            aboutSection.style.display =
                "block";

            loadingSection.style.display =
                "none";

            resultsSection.style.display =
                "none";

        }


        // -------------------------
        // MY MEMORIES
        // -------------------------

        else if (section === "memories") {

            heroSection.style.display =
                "none";

            aboutSection.style.display =
                "none";

            loadingSection.style.display =
                "none";

            resultsSection.style.display =
                "block";

        }

    });

});


// =====================================================
// LOGO → HOME
// =====================================================

if (logo) {

    logo.addEventListener("click", function () {

        const homeButton =
            document.querySelector(
                '[data-section="home"]'
            );

        if (homeButton) {

            homeButton.click();

        }

    });

}