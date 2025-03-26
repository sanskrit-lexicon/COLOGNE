document.addEventListener("DOMContentLoaded", function () {
    // Create search boxes dynamically
    const searchContainer = document.createElement("div");
    searchContainer.style.marginBottom = "10px";

    // Create transliteration dropdown
    const translitSelect = document.createElement("select");
    translitSelect.setAttribute("id", "translitSelect");
    translitSelect.style.marginRight = "10px";
    
    // Define available transliteration schemes
    const schemes = [
        "slp1", "devanagari", "bengali", "gujarati", "gurmukhi", "kannada",
        "malayalam", "oriya", "tamil", "telugu", "hk", "iast",
        "itrans", "kolkata", "velthuis", "wx"
    ];

    // Populate dropdown with scheme options
    schemes.forEach(scheme => {
        const option = document.createElement("option");
        option.value = scheme;
        option.textContent = scheme.charAt(0).toUpperCase() + scheme.slice(1);
        translitSelect.appendChild(option);
    });
    translitSelect.value = "slp1"; // Set default scheme to SLP1

    const searchHeadword = document.createElement("input");
    searchHeadword.setAttribute("type", "text");
    searchHeadword.setAttribute("placeholder", "Search in Headword (supports regex) (Case Sensitive)...");
    searchHeadword.setAttribute("id", "searchHeadword");
    searchHeadword.style.marginRight = "10px";
    
    const searchDefinition = document.createElement("input");
    searchDefinition.setAttribute("type", "text");
    searchDefinition.setAttribute("placeholder", "Search in Definition (supports regex) (Case Sensitive)...");
    searchDefinition.setAttribute("id", "searchDefinition");
    
    searchContainer.appendChild(translitSelect);
    searchContainer.appendChild(searchHeadword);
    searchContainer.appendChild(searchDefinition);
    document.body.insertBefore(searchContainer, document.body.firstChild);

    function applyTransliteration() {
        let selectedScheme = translitSelect.value;
        let sanskritElements = document.querySelectorAll(".sanskrit");
        sanskritElements.forEach(element => {
            element.textContent = Sanscript.t(element.getAttribute("data-original"), "slp1", selectedScheme);
        });
    }

    // Store original text content for transliteration updates
    document.querySelectorAll(".sanskrit").forEach(element => {
        element.setAttribute("data-original", element.textContent);
    });

    translitSelect.addEventListener("change", applyTransliteration);

    function highlightText(element, searchText, color) {
        if (!element) return;

        // Remove existing highlights first
        element.innerHTML = element.innerHTML.replace(/<span class="highlight-[a-z]+">|<\/span>/g, "");

        if (!searchText) return; // Prevents lingering highlights when search box is cleared

        try {
            let regex = new RegExp(searchText, "g"); // Case-sensitive regex

            function traverseNodes(node) {
                if (node.nodeType === Node.TEXT_NODE) {
                    let parent = node.parentNode;
                    let matches = node.nodeValue.match(regex);
                    if (matches) {
                        let temp = node.nodeValue.replace(regex, match => `<span class="highlight-${color}">${match}</span>`);
                        let tempElement = document.createElement("span");
                        tempElement.innerHTML = temp;
                        parent.replaceChild(tempElement, node);
                    }
                } else if (node.nodeType === Node.ELEMENT_NODE) {
                    [...node.childNodes].forEach(traverseNodes);
                }
            }

            // Traverse and apply highlighting only on text nodes
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

            if (headwordMatch && definitionMatch) { // Apply AND condition
                entry.style.display = "block";
                if (headwordMatch && headword) highlightText(headword, headwordText, "cyan");
                if (definitionMatch && definition) highlightText(definition, definitionText, "yellow");
            } else {
                entry.style.display = "none";
            }
        });
    }

    searchHeadword.addEventListener("input", filterEntries);
    searchDefinition.addEventListener("input", filterEntries);

    // Add CSS for highlighting
    const style = document.createElement("style");
    style.innerHTML = `
        .highlight-cyan { background-color: cyan; font-weight: bold; }
        .highlight-yellow { background-color: yellow; font-weight: bold; }
    `;
    document.head.appendChild(style);
});
