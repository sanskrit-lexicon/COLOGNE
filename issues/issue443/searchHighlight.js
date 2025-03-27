document.addEventListener("DOMContentLoaded", function () {
    // Create search & transliteration UI
    const searchContainer = document.createElement("div");
    searchContainer.style.position = "sticky";
    searchContainer.style.top = "0";
    searchContainer.style.backgroundColor = "white";
    searchContainer.style.padding = "10px";
    searchContainer.style.zIndex = "1000";
    searchContainer.style.borderBottom = "1px solid #ccc";
    searchContainer.style.display = "flex";
    searchContainer.style.alignItems = "center";
    searchContainer.style.gap = "10px";

    // Create transliteration dropdown
    const translitSelect = document.createElement("select");
    translitSelect.setAttribute("id", "translitSelect");

    const schemes = [
        "slp1", "devanagari", "bengali", "gujarati", "gurmukhi", "kannada",
        "malayalam", "oriya", "tamil", "telugu", "hk", "iast",
        "itrans", "kolkata", "velthuis", "wx"
    ];

    schemes.forEach(scheme => {
        const option = document.createElement("option");
        option.value = scheme;
        option.textContent = scheme.charAt(0).toUpperCase() + scheme.slice(1);
        translitSelect.appendChild(option);
    });
    translitSelect.value = "slp1"; // Default scheme

    // Create search inputs and buttons
    const searchHeadword = document.createElement("input");
    searchHeadword.setAttribute("type", "text");
    searchHeadword.setAttribute("placeholder", "Search in Headword...");
    searchHeadword.setAttribute("id", "searchHeadword");

    const nextHeadwordBtn = document.createElement("button");
    nextHeadwordBtn.textContent = "Next Match";

    const searchDefinition = document.createElement("input");
    searchDefinition.setAttribute("type", "text");
    searchDefinition.setAttribute("placeholder", "Search in Definition...");
    searchDefinition.setAttribute("id", "searchDefinition");

    const nextDefinitionBtn = document.createElement("button");
    nextDefinitionBtn.textContent = "Next Match";

    // Add elements to search container
    searchContainer.appendChild(translitSelect);
    searchContainer.appendChild(searchHeadword);
    searchContainer.appendChild(nextHeadwordBtn);
    searchContainer.appendChild(searchDefinition);
    searchContainer.appendChild(nextDefinitionBtn);
    document.body.insertBefore(searchContainer, document.body.firstChild);

    // Apply transliteration to Sanskrit, Headword, and Alt-Spelling
    function applyTransliteration() {
        let selectedScheme = translitSelect.value;
        document.querySelectorAll(".sanskrit, .headword, .alt-spelling").forEach(element => {
            element.textContent = Sanscript.t(element.getAttribute("data-original"), "slp1", selectedScheme);
        });
    }

    // Store original text for transliteration updates
    document.querySelectorAll(".sanskrit, .headword, .alt-spelling").forEach(element => {
        element.setAttribute("data-original", element.textContent);
    });

    translitSelect.addEventListener("change", applyTransliteration);

    function highlightText(element, searchText, color) {
        if (!element) return;
        element.innerHTML = element.innerHTML.replace(/<span class="highlight-[a-z]+">|<\/span>/g, "");

        if (!searchText) return;

        try {
            let regex = new RegExp(searchText, "g");

            function traverseNodes(node) {
                if (node.nodeType === Node.TEXT_NODE) {
                    let parent = node.parentNode;
                    if (node.nodeValue.match(regex)) {
                        let temp = node.nodeValue.replace(regex, match => `<span class="highlight-${color}">${match}</span>`);
                        let tempElement = document.createElement("span");
                        tempElement.innerHTML = temp;
                        parent.replaceChild(tempElement, node);
                    }
                } else if (node.nodeType === Node.ELEMENT_NODE) {
                    [...node.childNodes].forEach(traverseNodes);
                }
            }
            traverseNodes(element);
        } catch (e) {
            console.error("Invalid regex pattern:", e);
        }
    }

    function filterEntries() {
        let headwordText = searchHeadword.value.trim();
        let definitionText = searchDefinition.value.trim();
        let entries = document.querySelectorAll(".entry");

        entries.forEach(entry => {
            let headword = entry.querySelector(".headword");
            let definition = entry.querySelector(".definition");
            let headwordMatch = !headwordText || (headword && new RegExp(headwordText).test(headword.textContent));
            let definitionMatch = !definitionText || (definition && new RegExp(definitionText).test(definition.textContent));

            if (headwordMatch && definitionMatch) {
                entry.style.display = "block";
                if (headwordMatch && headword) highlightText(headword, headwordText, "cyan");
                if (definitionMatch && definition) highlightText(definition, definitionText, "yellow");
            } else {
                entry.style.display = "none";
            }
        });

        updateMatchLists();
    }

    let headwordMatches = [];
    let definitionMatches = [];
    let currentHeadwordIndex = -1;
    let currentDefinitionIndex = -1;

    function updateMatchLists() {
        headwordMatches = [...document.querySelectorAll(".highlight-cyan")];
        definitionMatches = [...document.querySelectorAll(".highlight-yellow")];
        currentHeadwordIndex = -1;
        currentDefinitionIndex = -1;
    }

    function scrollToNextMatch(matches, currentIndex) {
        if (matches.length === 0) return -1;

        currentIndex = (currentIndex + 1) % matches.length; // Loop back to first match after the last match

        let match = matches[currentIndex];
        match.scrollIntoView({ behavior: "smooth", block: "center" });

        return currentIndex;
    }

    nextHeadwordBtn.addEventListener("click", () => {
        currentHeadwordIndex = scrollToNextMatch(headwordMatches, currentHeadwordIndex);
    });

    nextDefinitionBtn.addEventListener("click", () => {
        currentDefinitionIndex = scrollToNextMatch(definitionMatches, currentDefinitionIndex);
    });

    searchHeadword.addEventListener("input", filterEntries);
    searchDefinition.addEventListener("input", filterEntries);

    const style = document.createElement("style");
    style.innerHTML = `
        .highlight-cyan { background-color: cyan; font-weight: bold; }
        .highlight-yellow { background-color: yellow; font-weight: bold; }
        body { padding-top: 60px; }
    `;
    document.head.appendChild(style);
});
