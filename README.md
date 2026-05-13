# HTML Utilities

![Project logo](https://raw.githubusercontent.com/NASA-JPL-Teamtools-Studio/teamtools_documentation/refs/heads/main/docs/images/tts_image_artifacts/html_utils.png)

## About Teamtools Studio

HTML Utilities is part of JPL's Teamtools Studio (TTS).

TTS is an effort originated in JPL's Planning and Execution section to centralize shared repositories across missions. This benefits JPL by reducing cost through reducing duplicated code, collaborating across missions, and unifying standards for development and design across JPL.

Although Planning and Execution is primarily concerned with flight operations, the TTS suite has been generalized and atomized to the point where many of these tools are applicable during other mission phases and even in non-spaceflight contexts. Through our work flying space missions, we hope to provide tools to the open source community that have utility in data analysis or planning for any complex system where failure is not an option.

For more infomation on how to contribute, and how these libraries form a complete ecosystem for high reliability data analysis, see the [Full TTS Documentation](https://nasa-jpl-teamtools-studio.github.io//teamtools_documentation/).

## What is HTML Utilities?

### Overview

HTML Utilities is what it says on the tin. While there are many HTML generating Pythonic libraries, the Teamtools Studio
team noticed that many do not match the patterns expected by purely Python developers, resulting in many difficult to
maintain HTML reporting tools all doing generally the same thing.

This library is intended to be much more Pythonic and provide the ability to create somewhat sophisticated HTML reports
with little specific web design knowledge. There is also some JavaScript embedded in some entities to enable a light level
of interactivity needed for this work.

The core capability of this library is to facilitate the generation of single-page HTML reports of spacecraft data that
can be emailed or attached to other reporting systems. That being said, there is no reason this library couldn't be used
for simple UI applications of the type sometimes built by Teamtools developers on JPL missions.

This library uses components that look and feel more or less like Plotly Dash, but is not meant to necessarily be as
sophisticated as that library, and unlike Plotly Dash, it is meant to be used as a standalone HTML report generation tool.

While it certainly can be--and indeed is--used as a component in web applications, its primary use case is to create
components to be incorporated into HTML-friendly applications like Confluence, or to just make custom reports as HTML files
that can be easily shared via email or attaching to other reporting and project management tools like Jira.

### Projects Currently Supported

* Europa Clipper
* Mars 2020/Perseverance
* Mars Sample Return/Sample Retrieval Lander
* Mars Science Laboratory/Curiosity
* Mars Reconnaisance Orbiter
* NISAR
* Orbiting Carbon Observatory 2 (OCO-2)

## Architecture

### TTS dependencies

* TTS Utilities