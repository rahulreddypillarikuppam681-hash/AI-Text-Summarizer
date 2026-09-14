const textInput =
    document.getElementById("textInput");

const summarizeBtn =
    document.getElementById("summarizeBtn");

const summary =
    document.getElementById("summary");

const loading =
    document.getElementById("loading");

const loadingText =
    document.getElementById("loadingText");

const wordCount =
    document.getElementById("wordCount");

const copyBtn =
    document.getElementById("copyBtn");

const summaryLength =
    document.getElementById("summaryLength");

const summaryFormat =
    document.getElementById("summaryFormat");

const fileInput =
    document.getElementById("fileInput");

const fileName =
    document.getElementById("fileName");


// ==========================================
// Word counter
// ==========================================

function updateWordCount() {

    const text =
        textInput.value.trim();


    const words =
        text === ""
            ? 0
            : text.split(/\s+/).length;


    wordCount.textContent =
        `${words} words`;
}


textInput.addEventListener(
    "input",
    updateWordCount
);


// ==========================================
// TXT file upload
// ==========================================

fileInput.addEventListener(
    "change",
    async () => {

        const file =
            fileInput.files[0];


        if (!file) {
            return;
        }


        fileName.textContent =
            "Reading file...";


        const formData =
            new FormData();


        formData.append(
            "file",
            file
        );


        try {

            const response =
                await fetch(
                    "/upload",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    data.error ||
                    "Could not upload file."
                );

            }


            textInput.value =
                data.text;


            updateWordCount();


            fileName.textContent =
                `✅ ${data.filename}`;


        } catch (error) {

            console.error(error);


            fileName.textContent =
                "❌ Upload failed";


            alert(
                error.message
            );

        }

    }
);


// ==========================================
// Summarize
// ==========================================

summarizeBtn.addEventListener(
    "click",
    async () => {


        const text =
            textInput.value.trim();


        const length =
            summaryLength.value;


        const format =
            summaryFormat.value;


        // ----------------------------------
        // Validate text
        // ----------------------------------

        if (!text) {

            alert(
                "Please enter some text first."
            );

            return;

        }


        // ----------------------------------
        // Count words
        // ----------------------------------

        const totalWords =
            text.split(/\s+/).length;


        // ----------------------------------
        // Show loading
        // ----------------------------------

        loading.classList.remove(
            "hidden"
        );


        summarizeBtn.disabled =
            true;


        if (totalWords > 2500) {

            loadingText.textContent =
                "AI is processing your long document...";

        } else {

            loadingText.textContent =
                "AI is creating your summary...";

        }


        summary.innerHTML = `
            <p class="placeholder">
                AI is creating your summary...
            </p>
        `;


        try {

            const response =
                await fetch(
                    "/summarize",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            text: text,

                            length: length,

                            format: format

                        })

                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Server error."
                );

            }


            // --------------------------------
            // Display summary
            // --------------------------------

            summary.textContent =
                data.summary;


        } catch (error) {

            console.error(error);


            summary.innerHTML = `
                <p class="placeholder">
                    ❌ ${error.message}
                </p>
            `;


        } finally {

            loading.classList.add(
                "hidden"
            );


            summarizeBtn.disabled =
                false;


            loadingText.textContent =
                "AI is creating your summary...";

        }

    }
);


// ==========================================
// Copy summary
// ==========================================

copyBtn.addEventListener(
    "click",
    async () => {


        const text =
            summary.textContent.trim();


        if (
            !text ||
            text ===
            "Your AI-generated summary will appear here."
        ) {

            return;

        }


        try {

            await navigator.clipboard
                .writeText(text);


            copyBtn.textContent =
                "✅ Copied!";


            setTimeout(
                () => {

                    copyBtn.textContent =
                        "📋 Copy";

                },
                1500
            );


        } catch (error) {

            console.error(error);


            alert(
                "Could not copy the summary."
            );

        }

    }
);