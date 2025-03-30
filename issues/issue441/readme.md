# README

This repository contains resources for transforming XML data into an HTML document using XSLT. The transformation enhances Sanskrit dictionary entries, applies formatting, expands abbreviations, and generates links using reference data from `abs.xml`.

---

## **Files in This Directory**

- **`abs.xml`**: A reference XML file containing a list of abbreviations (short forms of book names) and their corresponding full names and links.  
- **`test.xml`**: The main input XML file containing Sanskrit dictionary entries that need to be transformed.  
- **`transform.xsl`**: The XSLT stylesheet defining the transformation rules to be applied to `test.xml`.  
- **`output.html`**: The resulting HTML document after applying the XSL transformation to `test.xml`.  

---

## **How to Use**

To perform the transformation, follow these steps:

1. **Ensure you have an XSLT processor installed**  
   You can use any XSLT processor, such as:
   - **xsltproc** (command-line tool from `libxslt`)
   - **Saxon** (Java-based XSLT processor)
   - **Xalan** (Apache's XSLT processor)

2. **Execute the transformation using `xsltproc`**  
   Run the following command in your terminal:

   ```bash
   xsltproc transform.xsl test.xml -o output.html
   ```

   This command applies the `transform.xsl` stylesheet to `test.xml` and outputs the result to `output.html`.

3. **Open `output.html`**  
   Once the transformation is complete, open `output.html` in a web browser to view the formatted output.

---

## **Transformations Performed by `transform.xsl`**

The `transform.xsl` stylesheet is responsible for converting `test.xml` into a structured HTML document. It applies formatting, expands abbreviations using `abs.xml`, and generates hyperlinks for book references.

### **1. HTML Document Structure Creation**
- **Output Method Specification**: The stylesheet specifies HTML as the output format and enables indentation.
  ```xml
  <xsl:output method="html" indent="yes"/>
  ```
- **HTML Skeleton Construction**: It constructs the basic structure of the HTML document.
  ```xml
  <html>
    <head>
      <meta charset="UTF-8"/>
      <title>Sanskrit Dictionary</title>
      <style> /* CSS for styling the output */ </style>
    </head>
    <body>
      <xsl:apply-templates/>
    </body>
  </html>
  ```

### **2. Processing Dictionary Entries**
- Each `<entry>` element in `test.xml` is converted into a styled `<div>` with the dictionary headword, alternate spellings, and definitions.
  ```xml
  <xsl:template match="entry">
    <div class="entry">
      <span class="headword"><xsl:value-of select="h"/></span>
      <xsl:if test="alt">
        <span class="alt-spelling"> (<xsl:value-of select="alt"/>)</span>
      </xsl:if>
      <div class="definition">
        <xsl:apply-templates select="body"/>
      </div>
    </div>
  </xsl:template>
  ```

### **3. Expanding Abbreviations (`ab`) Using `abs.xml`**
- The transformation cross-references abbreviations (`<ab>`) in `test.xml` with `abs.xml` to replace short forms with full names.
  ```xml
  <xsl:template match="ab">
    <xsl:variable name="abbr" select="."/>
    <xsl:variable name="fullForm" select="document('abs.xml')//abbreviation[abbr = $abbr]/full"/>
    <xsl:choose>
      <xsl:when test="$fullForm">
        <span class="tooltip">
          <xsl:value-of select="$abbr"/>
          <span class="tooltiptext"><xsl:value-of select="$fullForm"/></span>
        </span>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$abbr"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  ```

### **4. Generating Links for `<ls>` (Literary Sources)**
- `<ls>` elements represent references to books, which are stored in `abs.xml`. The transformation converts these into hyperlinks.
  ```xml
  <xsl:template match="ls">
    <xsl:variable name="refId" select="."/>
    <xsl:variable name="bookLink" select="document('abs.xml')//ref[@id=$refId]/link"/>
    <xsl:variable name="bookName" select="document('abs.xml')//ref[@id=$refId]/full-name"/>
    <a href="{$bookLink}" target="_blank">
      <xsl:value-of select="$bookName"/>
    </a>
  </xsl:template>
  ```

### **5. Formatting Other Elements**
- **Italicization (`i`)**: Converts `<i>` elements into `<em>`.
  ```xml
  <xsl:template match="i">
    <em><xsl:apply-templates/></em>
  </xsl:template>
  ```
- **Bold Formatting (`b`)**: Converts `<b>` elements into `<strong>`.
  ```xml
  <xsl:template match="b">
    <strong><xsl:apply-templates/></strong>
  </xsl:template>
  ```
- **Line Breaks (`lb`)**: Converts `<lb/>` elements into `<br/>`.
  ```xml
  <xsl:template match="lb">
    <br/>
  </xsl:template>
  ```

---

## **Dependencies**
- **XSLT Processor**: You need `xsltproc` (or an equivalent processor).
  - On **Ubuntu/Debian**:
    ```bash
    sudo apt install xsltproc
    ```
  - On **macOS**:
    ```bash
    brew install libxslt
    ```
  - On **Windows**, install `xsltproc` via Cygwin or use Saxon:
    ```bash
    java -jar saxon.jar -s:test.xml -xsl:transform.xsl -o:output.html
    ```

---

## **Summary**
1. **Extracts data from `test.xml`**: Processes dictionary entries, abbreviations, and book references.  
2. **Generates an HTML structure**: Wraps extracted content in styled `<div>` elements.  
3. **Expands abbreviations**: Uses `abs.xml` to replace short forms with full names and tooltips.  
4. **Creates hyperlinks for `<ls>` elements**: Converts book references into clickable links using `abs.xml`.  
5. **Applies formatting**: Handles bold, italic, and line break elements.  
6. **Produces a complete `output.html` file** that is styled and structured for easy viewing.  

By following these instructions, you can successfully transform `test.xml` into `output.html` using XSLT.

