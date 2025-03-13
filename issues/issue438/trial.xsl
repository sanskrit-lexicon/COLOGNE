<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>

    <xsl:variable name="abbrDoc" select="document('abbreviations.xml')"/>

    <xsl:template match="/">
        <html>
            <head>
                <meta charset="UTF-8"/>
            </head>
            <body>
                <div id='CologneBasic'>
                    <xsl:apply-templates/>
                </div>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="pwg">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="H1">
        <h1>&#160;<span class='sdata_siddhanta'><xsl:value-of select="h/key1"/></span></h1>
        <table class='display'>
            <tr>
                <td class='display' valign="top">
                    <span style='font-weight:bold'>
                        <span class='sdata'><xsl:value-of select="h/key1"/></span>
                        <span class='hrefdata'>
                            <span style='font-weight:normal; color:rgb(160,160,160);'>
                                [Printed book page <a href='//www.sanskrit-lexicon.uni-koeln.de/scans/csl-apidev/servepdf.php?dict=PWG&amp;page={tail/pc}' target='_PWG'>
                                    <xsl:value-of select="tail/pc"/>
                                </a>]
                            </span>
                        </span>
                    </span>
                    <br/>
                    <span class='sdata_siddhanta'><xsl:value-of select="h/key1"/></span>
                    <xsl:apply-templates select="body"/>
                </td>
            </tr>
        </table>
    </xsl:template>

    <xsl:template match="body">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="div">
        <div style='padding-left:{@n}em;'>
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="s">
        <span class="sdata_siddhanta">
            <xsl:value-of select="."/>
        </span>
    </xsl:template>

    <xsl:template match="ls">
        <xsl:variable name="abbrFull" select="normalize-space(.)"/>
        <xsl:variable name="abbrCleaned" select="translate($abbrFull, '0123456789,', '')"/>
        <xsl:variable name="tooltip" select="$abbrDoc/data/lslist/ls[ss = $abbrCleaned]/ff"/>
        <span class="tooltip">
            <xsl:attribute name="title">
                <xsl:value-of select="$tooltip"/>
            </xsl:attribute>
            <xsl:value-of select="$abbrFull"/>
        </span>
    </xsl:template>
</xsl:stylesheet>
