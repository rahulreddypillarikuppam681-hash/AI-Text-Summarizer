const textInput = document.getElementById("textInput");
const summarizeBtn = document.getElementById("summarizeBtn");
const summary = document.getElementById("summary");
const loading = document.getElementById("loading");
const wordCount = document.getElementById("wordCount");
const copyBtn = document.getElementById("copyBtn");


// Word counter
textInput.addEventListener("input", () => {
    const text = textInput.value.trim();

    const words = text === ""
        ? 0
        : text.split(/\s+/).length;

    wordCount.textContent = `${words} words`;
});


// Summarize button
summarizeBtn.addEventListener("click", async () => {

    const text = textInput.value.trim();

    if (!text) {
        alert("Please enter some text first.");
        return;
    }

    loading.classList.remove("hidden");
    summarizeBtn.disabled = true;
    summary.textContent = "Generating summary...";

    try {

        const response = await fetch("http://127.0.0.1:8000/summarize", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text
            })
        });

        if (!response.ok) {
            throw new Error("Failed to summarize text.");
        }

        const data = await response.json();

        summary.textContent = data.summary;

    } catch (error) {

        console.error(error);

        summary.textContent =
            "Something went wrong. Make sure the FastAPI server is running.";

    } finally {

        loading.classList.add("hidden");
        summarizeBtn.disabled = false;

    }
});


// Copy summary
copyBtn.addEventListener("click", async () => {

    const text = summary.textContent;

    if (!text || text === "Your summary will appear here...") {
        return;
    }

    await navigator.clipboard.writeText(text);

    copyBtn.textContent = "✅ Copied!";

    setTimeout(() => {
        copyBtn.textContent = "📋 Copy Summary";
    }, 1500);
});