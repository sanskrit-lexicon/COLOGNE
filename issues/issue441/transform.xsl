<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" indent="yes"/>
    <xsl:variable name="absData" select="document('abs.xml')"/>
    
    <xsl:template match="/pwg">
        <html>
            <head>
                <meta charset="UTF-8"/>
                <title>Sanskrit Dictionary</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; }
                    .entry { margin-bottom: 20px; padding: 15px; background: white; border-radius: 8px; box-shadow: 2px 2px 5px gray; }
                    .headword { font-size: 24px; font-weight: bold; color: #333; }
                    .alt-spelling { font-size: 18px; color: #555; }
                    .metadata { font-size: 14px; color: #777; margin-top: 5px; }
                    .definition { margin-left: 20px; font-size: 16px; }
                    .sanskrit { font-family: 'Devanagari', serif; color: darkred; display: inline; }
                    .citation { font-family: monospace; color: #0066cc; display: inline; margin-left: 5px; }
                    .source { font-size: 14px; color: #777; }
                    .indent-1 { margin-left: 20px; }
                    .indent-2 { margin-left: 40px; }
                    .indent-4 { margin-left: 80px; display: inline-block; }
                    .ls-reference { font-family: 'Times New Roman', serif; color: blue; display: inline; margin-left: 5px; }
                </style>
            </head>
            <body>
                <h1>Sanskrit Dictionary</h1>
                <xsl:apply-templates select="H1"/>
            </body>
        </html>
    </xsl:template>
    
    <xsl:template match="H1">
        <div class="entry">
            <div class="headword">
                <xsl:value-of select="h/key1"/>
            </div>
            <div class="alt-spelling">
                <xsl:value-of select="h/key2"/>
            </div>
            <div class="metadata">
                <xsl:text>L=</xsl:text><xsl:value-of select="tail/L"/> | 
                <xsl:text>page=</xsl:text>
                <a href="https://www.sanskrit-lexicon.uni-koeln.de/scans/csl-apidev/servepdf.php?dict=PWG&amp;page={tail/pc}" target="_blank">
                    <xsl:value-of select="tail/pc"/>
                </a>
            </div>
            <div class="definition">
                <xsl:apply-templates select="body"/>
            </div>
        </div>
    </xsl:template>
    
    <xsl:template match="body">
        <xsl:apply-templates/>
    </xsl:template>
    
    <xsl:template match="s">
        <br/>
        <div class="indent-4">
            <span class="sanskrit">
                <xsl:value-of select="."/>
            </span>
            <!-- Apply only the first consecutive <ls> elements directly after <s> -->
            <xsl:apply-templates select="following-sibling::ls[not(preceding-sibling::s)]"/>
        </div>
    </xsl:template>

    <xsl:template match="div">
        <xsl:variable name="class">
            <xsl:choose>
                <xsl:when test="@n='1'">indent-1</xsl:when>
                <xsl:when test="@n='2'">indent-2</xsl:when>
                <xsl:otherwise></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <div class="{$class}">
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    <xsl:template match="ls">
        <xsl:variable name="source" select="@n"/>
        <xsl:variable name="id" select="@id"/>
        <xsl:variable name="formatted-id">
            <xsl:value-of select="normalize-space(translate($id, ' ', ''))"/>
        </xsl:variable>
        <xsl:variable name="link" select="$absData/abs/lsd[ss=$source]/link"/>
        
        <xsl:choose>
            <!-- If a corresponding entry exists in abs.xml -->
            <xsl:when test="$link and $id">
                <a href="{$link}?{$formatted-id}" class="ls-reference" target="_blank">
                    [<xsl:value-of select="$source"/> <xsl:text> </xsl:text><xsl:value-of select="$formatted-id"/>]
                </a>
            </xsl:when>
            <!-- If no matching entry in abs.xml, fallback to standard formatting -->
            <xsl:when test="@n and @id">
                <span class="ls-reference">[<xsl:value-of select="@n"/> <xsl:text> </xsl:text><xsl:value-of select="$formatted-id"/>]</span>
            </xsl:when>
            <!-- If neither @n nor @id exist, just show the text inside ls -->
            <xsl:otherwise>
                <span class="ls-reference">[<xsl:value-of select="."/>]</span>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
