<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" indent="yes"/>
    
    <xsl:template match="/pwg">
        <html>
            <head>
                <title>Sanskrit Dictionary</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; }
                    .entry { margin-bottom: 20px; padding: 15px; background: white; border-radius: 8px; box-shadow: 2px 2px 5px gray; }
                    .headword { font-size: 24px; font-weight: bold; color: #333; }
                    .alt-spelling { font-size: 18px; color: #555; }
                    .definition { margin-left: 20px; font-size: 16px; }
                    .sanskrit { font-family: 'Devanagari', serif; color: darkred; }
                    .citation { font-style: italic; color: #0066cc; }
                    .source { font-size: 14px; color: #777; }
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
        </div>
    </xsl:template>
    
    <xsl:template match="body">
        <xsl:apply-templates/>
    </xsl:template>
    
    <xsl:template match="s">
        <div class="sanskrit">
            <xsl:value-of select="."/>
        </div>
    </xsl:template>
    
    <xsl:template match="ls">
        <span class="citation">
            <xsl:value-of select="@n"/> - <xsl:value-of select="@id"/>
        </span>
    </xsl:template>
</xsl:stylesheet>
