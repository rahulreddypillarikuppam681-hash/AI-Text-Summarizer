const textInput = document.getElementById("textInput");
const summarizeBtn = document.getElementById("summarizeBtn");
const summary = document.getElementById("summary");
const loading = document.getElementById("loading");
const wordCount = document.getElementById("wordCount");
const copyBtn = document.getElementById("copyBtn");

const summaryLength = document.getElementById("summaryLength");
const summaryFormat = document.getElementById("summaryFormat");


// ----------------------------------
// Word counter
// ----------------------------------

textInput.addEventListener("input", () => {

    const text = textInput.value.trim();

    const words = text === ""
        ? 0
        : text.split(/\s+/).length;

    wordCount.textContent = `${words} words`;

});


// ----------------------------------
// Summarize
// ----------------------------------

summarizeBtn.addEventListener("click", async () => {

    const text = textInput.value.trim();

    const length = summaryLength.value;

    const format = summaryFormat.value;


    // Check empty text

    if (!text) {

        alert("Please enter some text first.");

        return;
    }


    // Loading state

    loading.classList.remove("hidden");

    summarizeBtn.disabled = true;

    summary.innerHTML = `
        <p class="placeholder">
            AI is creating your summary...
        </p>
    `;


    try {

        const response = await fetch("/summarize", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                text: text,

                length: length,

                format: format

            })

        });


        if (!response.ok) {

            throw new Error(
                `Server error: ${response.status}`
            );

        }


        const data = await response.json();


        summary.textContent = data.summary;


    } catch (error) {

        console.error(error);

        summary.innerHTML = `
            <p class="placeholder">
                Something went wrong. Please try again.
            </p>
        `;

    } finally {

        loading.classList.add("hidden");

        summarizeBtn.disabled = false;

    }

});


// ----------------------------------
// Copy summary
// ----------------------------------

copyBtn.addEventListener("click", async () => {

    const text = summary.textContent.trim();


    if (
        !text ||
        text === "Your AI-generated summary will appear here."
    ) {

        return;

    }


    try {

        await navigator.clipboard.writeText(text);

        copyBtn.textContent = "✅ Copied!";


        setTimeout(() => {

            copyBtn.textContent = "📋 Copy";

        }, 1500);


    } catch (error) {

        console.error(error);

        alert("Could not copy the summary.");

    }

});