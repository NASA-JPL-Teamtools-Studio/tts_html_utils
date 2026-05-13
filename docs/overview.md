# HTML Utilities

![Project logo](https://raw.githubusercontent.com/NASA-JPL-Teamtools-Studio/teamtools_documentation/refs/heads/main/docs/images/tts_image_artifacts/html_utils.png)

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