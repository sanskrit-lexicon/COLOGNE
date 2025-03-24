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
                    .definition { margin-left: 20px; font-size: 16px; }
                    .sanskrit { font-family: 'Devanagari', serif; color: darkred; display: inline; }
                    .citation { font-family: monospace; color: #0066cc; display: inline; margin-left: 5px; }
                    .source { font-size: 14px; color: #777; }
                    .indent-1 { margin-left: 20px; }
                    .indent-2 { margin-left: 40px; }
                    .indent-4 { margin-left: 80px; display: inline-block; }
                    .ls-reference { font-family: 'Times New Roman', serif; color: lightgray; display: inline; margin-left: 5px; }
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
            <div class="definition">
                <xsl:apply-templates select="body"/>
            </div>
            <div class="L">
                <xsl:value-of select="tail/L"/>
            </div>
            <div class="pc">
                <xsl:value-of select="tail/pc"/>
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
        <xsl:variable name="link" select="$absData/abs/lss[ss=$source]/link"/>
        
        <xsl:choose>
            <!-- If a corresponding entry exists in abs.xml -->
            <xsl:when test="$link and $id">
                <a href="https://sanskrit-lexicon-scans.github.io/{$link}/?{$id}">
                    [<xsl:value-of select="$source"/> <xsl:value-of select="$id"/>]
                </a>
            </xsl:when>
            <!-- If no matching entry in abs.xml, fallback to standard formatting -->
            <xsl:when test="@n and @id">
                <span class="ls-reference">[<xsl:value-of select="@n"/> <xsl:value-of select="@id"/>]</span>
            </xsl:when>
            <!-- If neither @n nor @id exist, just show the text inside ls -->
            <xsl:otherwise>
                <span class="ls-reference">[<xsl:value-of select="."/>]</span>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
