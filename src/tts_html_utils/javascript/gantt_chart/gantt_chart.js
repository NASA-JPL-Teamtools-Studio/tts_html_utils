document.addEventListener('DOMContentLoaded', function() {
  setTimeout(function() {
    (function() {
        // Debug logging to see what data is being passed
        let rawData = {{ chart_data_json | safe }};
        console.log('Raw data:', rawData);
    
    // Check if data is empty or invalid, provide fallback if needed
    if (!rawData || !Array.isArray(rawData) || rawData.length === 0) {
        console.warn('No valid data found, using fallback data');
        // Provide fallback data
        rawData = [
            {
                "name": "Example Task",
                "start": "2024-01-01T09:00:00",
                "end": "2024-01-01T17:00:00",
                "children": [
                    {
                        "name": "Subtask 1",
                        "start": "2024-01-01T09:00:00",
                        "end": "2024-01-01T12:00:00"
                    },
                    {
                        "name": "Subtask 2",
                        "start": "2024-01-01T13:00:00",
                        "end": "2024-01-01T17:00:00"
                    }
                ]
            }
        ];
    }
    const uniqueId = "{{ unique_id }}";
    const initialInnerWidth = parseInt("{{ inner_width }}".replace('px', ''));
    // Set default_depth to -1 to make all activities collapsed by default
    const defaultDepth = parseInt("{{ default_depth }}") || -1; // Use the default_depth parameter from context, default to -1
    
    // Parse input dates with validation - using UTC to prevent DST issues
    let startDate = new Date("{{ start_date }}Z").getTime(); // Z suffix forces UTC
    let endDate = new Date("{{ end_date }}Z").getTime(); // Z suffix forces UTC
    if (isNaN(startDate)) startDate = new Date().getTime();
    if (isNaN(endDate)) endDate = startDate + 86400000;
    
    // Add padding to the timeline (5% on each side)
    const rawDuration = endDate - startDate;
    const padding = rawDuration * 0.05;
    startDate -= padding;
    endDate += padding;
    
    // Define time constants first
    const MS_SEC = 1000;
    const MS_MIN = 60 * MS_SEC;
    const MS_HOUR = 60 * MS_MIN;
    const MS_DAY = 24 * MS_HOUR;
    
    // Store both the padded and original bounds
    const totalTime = endDate - startDate;
    const originalStartDate = startDate + padding;
    const originalEndDate = endDate - padding;

    // Get DOM elements first
    const sidebarListEl = document.getElementById(`sidebar-list-${uniqueId}`);
    const barsContainerEl = document.getElementById(`bars-${uniqueId}`);
    const axisEl = document.getElementById(`axis-${uniqueId}`);
    const gridEl = document.getElementById(`grid-${uniqueId}`);
    const canvasEl = document.getElementById(`canvas-${uniqueId}`);
    const tooltipEl = document.getElementById(`tooltip-${uniqueId}`);
    const statusEl = document.getElementById(`status-${uniqueId}`);
    const tlHeaderEl = document.getElementById(`tl-header-${uniqueId}`);
    const scrollAreaEl = document.getElementById(`timeline-scroll-${uniqueId}`);
    const cursorTimeEl = document.getElementById(`cursor-time-${uniqueId}`);
    const viewRangeEl = document.getElementById(`view-range-${uniqueId}`);
    
    // Calculate zoom limits
    const minZoom = initialInnerWidth / totalTime; // Fit entire timeline
    
    // Calculate max zoom based on minimum visible time span (half an hour)
    // This ensures at least 30 minutes are visible on screen at maximum zoom
    const minVisibleTimeSpan = MS_MIN * 30; // 30 minutes minimum visible timespan
    const maxZoom = scrollAreaEl ? scrollAreaEl.clientWidth / minVisibleTimeSpan : initialInnerWidth / minVisibleTimeSpan;

    let currentZoom = 1.0;
    let pixelsPerMS = initialInnerWidth / totalTime;

    // --- Tick Config ---

    const TICK_STEPS = [
        { ms: MS_DAY * 365, label: "Year" },
        { ms: MS_DAY * 30,  label: "Month" },
        { ms: MS_DAY * 7,   label: "Week" },
        { ms: MS_DAY,       label: "Day" },
        { ms: MS_HOUR * 12, label: "12 Hr" },
        { ms: MS_HOUR * 6,  label: "6 Hr" },
        { ms: MS_HOUR * 3,  label: "3 Hr" },
        { ms: MS_HOUR,      label: "Hour" },
        { ms: MS_MIN * 15,  label: "15 M" },
        { ms: MS_MIN * 5,   label: "5 M" },
        { ms: MS_MIN,       label: "Min" },
        { ms: MS_SEC * 30,  label: "30 S" },
        { ms: MS_SEC * 15,  label: "15 S" },
        { ms: MS_SEC * 5,   label: "5 S" },
        { ms: MS_SEC,       label: "Sec" },
    ];

    // --- Formatters --- using UTC methods to prevent DST issues
    const formatTime = (date) => date.getUTCHours().toString().padStart(2,'0') + ':' + date.getUTCMinutes().toString().padStart(2,'0');
    const formatSec = (date) => formatTime(date) + ':' + date.getUTCSeconds().toString().padStart(2,'0');
    const formatDay = (date) => date.toLocaleString('default', { month: 'short', timeZone: 'UTC' }) + ' ' + date.getUTCDate();
    const formatFull = (date) => date.getUTCFullYear() + '-' + (date.getUTCMonth()+1).toString().padStart(2,'0') + '-' + date.getUTCDate().toString().padStart(2,'0');

    function getTickLabel(date, stepLabel) {
        const isMidnight = (date.getUTCHours() === 0 && date.getUTCMinutes() === 0 && date.getUTCSeconds() === 0);
        const isMonthStart = (date.getUTCDate() === 1 && isMidnight);

        if (["12 Hr", "6 Hr", "3 Hr", "Hour", "15 M", "5 M", "Min"].includes(stepLabel)) {
            if (isMidnight) return formatDay(date); 
            return formatTime(date);
        }
        if (["30 S", "15 S", "5 S", "Sec"].includes(stepLabel)) {
            if (isMidnight) return formatDay(date);
            return formatSec(date);
        }
        if (stepLabel === "Day") return isMonthStart ? date.toLocaleString('default', { month: 'short', year: '2-digit', timeZone: 'UTC'}) : formatDay(date);
        if (stepLabel === "Month") return date.toLocaleString('default', { month: 'long', year: '2-digit', timeZone: 'UTC'});
        if (stepLabel === "Year") return date.getUTCFullYear();
        if (stepLabel === "Week") return (date.getUTCMonth()+1) + '/' + date.getUTCDate();

        return date.toLocaleDateString(undefined, {timeZone: 'UTC'});
    }
    
    function formatRangeDate(t) {
        const d = new Date(t);
        if (pixelsPerMS < 0.00001) return formatFull(d); 
        if (pixelsPerMS < 0.01) return formatFull(d) + " " + formatTime(d);
        return formatFull(d) + " " + formatSec(d);
    }

    // --- Axis Rendering ---
    function drawAxis() {
        const currentWidth = totalTime * pixelsPerMS;
        // Don't set width here anymore to avoid redundant layout thrashing, 
        // handled in applyZoom or init.
        // Actually we need to set it for initial load.
        // But in applyZoom we set it explicitly before scrolling.
        
        const scrollLeft = scrollAreaEl.scrollLeft;
        const viewWidth = scrollAreaEl.clientWidth;
        
        // Update View Range Text
        const viewStartMs = startDate + (scrollLeft / pixelsPerMS);
        const viewEndMs = startDate + ((scrollLeft + viewWidth) / pixelsPerMS);
        viewRangeEl.innerText = `${formatRangeDate(viewStartMs)}  —  ${formatRangeDate(viewEndMs)}`;
        
        // Find appropriate tick step based on zoom level
        // Start with the smallest time unit as default
        let activeStep = TICK_STEPS[TICK_STEPS.length - 1]; // Default to smallest step (Second)
        
        // Calculate ideal tick spacing in pixels (aim for ~100px between major ticks)
        const idealTickSpacingPx = 100;
        const idealTickSpacingMs = idealTickSpacingPx / pixelsPerMS;
        
        // Find the closest matching step
        let bestDiff = Infinity;
        
        for (let i = 0; i < TICK_STEPS.length; i++) {
            const step = TICK_STEPS[i];
            const diff = Math.abs(step.ms - idealTickSpacingMs);
            
            // If this step is closer to ideal spacing than our current best
            if (diff < bestDiff) {
                bestDiff = diff;
                activeStep = step;
            }
        }
        statusEl.innerText = `Zoom: ${activeStep.label}`;

        // Clear
        axisEl.innerHTML = '';
        gridEl.innerHTML = '';

        // Calculate virtual render range with extra buffer for smooth scrolling
        // We render more than what's visible to allow smooth scrolling
        const bufferPx = Math.max(500, viewWidth * 0.5); // Buffer of 500px or half viewport, whichever is larger
        
        // Ensure we don't render outside the actual timeline bounds
        const renderStartPx = Math.max(0, scrollLeft - bufferPx);
        const renderEndPx = Math.min(currentWidth, scrollLeft + viewWidth + bufferPx);

        // Convert pixel positions to time values
        const renderStartTime = startDate + (renderStartPx / pixelsPerMS);
        const renderEndTime = startDate + (renderEndPx / pixelsPerMS);

        // Round to nearest tick step to ensure consistent tick placement
        const startRounded = Math.floor(renderStartTime / activeStep.ms) * activeStep.ms;

        for (let t = startRounded; t <= renderEndTime; t += activeStep.ms) {
            const pct = (t - startDate) / totalTime;
            const leftPx = pct * currentWidth;
            
            const dateObj = new Date(t);
            const labelText = getTickLabel(dateObj, activeStep.label);
            
            const isMidnight = (dateObj.getHours() === 0 && dateObj.getMinutes() === 0 && dateObj.getSeconds() === 0);
            let isMajor = (activeStep.ms < MS_DAY && isMidnight) || (activeStep.label === "Day" && dateObj.getDate()===1);

            const tick = document.createElement('div');
            tick.className = 'gantt-tick' + (isMajor ? ' major-tick' : '');
            tick.style.left = leftPx + 'px';
            tick.innerText = labelText;
            axisEl.appendChild(tick);

            const grid = document.createElement('div');
            grid.className = 'gantt-grid-line' + (isMajor ? ' major-grid' : '');
            grid.style.left = leftPx + 'px';
            gridEl.appendChild(grid);
        }
    }

    // --- Flatten & Render ---
    let flatTasks = [];
    function flatten(items, depth, parentId) {
        items.forEach((item, index) => {
            const internalId = parentId ? parentId + "-" + index : "root-" + index;
            // Expand items based on their depth and the defaultDepth parameter
            // Items with depth <= defaultDepth are expanded by default
            // With defaultDepth set to -1, all items will be collapsed by default
            const isExpanded = depth <= defaultDepth;
            const task = {
                id: internalId, parentId, name: item.name,
                start: item.start ? new Date(item.start + "Z").getTime() : null,
                end: item.end ? new Date(item.end + "Z").getTime() : null,
                color: item.color, // Include the color property
                highlight_full_height: item.highlight_full_height || false, // Include the highlight_full_height property
                below_the_fold: item.below_the_fold || false, // Include the below_the_fold property
                hover_text: item.hover_text, // Include custom hover text
                children: item.children || [],
                depth, expanded: isExpanded,
                hasChildren: (item.children && item.children.length > 0)
            };
            flatTasks.push(task);
            if (task.hasChildren) flatten(task.children, depth + 1, internalId);
        });
    }
    flatten(rawData, 0, null);
    console.log('Flattened tasks:', flatTasks);
    
    // No sorting here - we'll use the order from the JSON
    // This ensures activities appear in the exact order they were provided
    
    // Debug log to show which tasks will be visible
    console.log('Visible tasks:', flatTasks.filter(task => shouldShow(task)).map(task => ({ name: task.name, depth: task.depth, expanded: task.expanded })));

    function shouldShow(task) {
        // Root tasks (depth 0) are always shown
        if (!task.parentId) return true;
        
        // For all other tasks, check if their parent is expanded
        const parent = flatTasks.find(t => t.id === task.parentId);
        
        // If parent doesn't exist or isn't expanded, don't show this task
        if (!parent || !parent.expanded) return false;
        
        // If parent is expanded and visible, show this task
        return shouldShow(parent);
    }

    function renderRows() {
        sidebarListEl.innerHTML = '';
        barsContainerEl.innerHTML = '';
        
        const currentWidth = totalTime * pixelsPerMS;
        const axisHeight = 40;
        const rowHeight = 35; // Fixed row height for consistency 
        let visibleIndex = 0;
        
        // Create a map to track parent activities and their children
        const parentGroups = {};
        
        // Track if we've seen a below-the-fold task yet
        let lastWasAboveTheFold = true;
        let separatorAdded = false;

        flatTasks.forEach(task => {
            if (!shouldShow(task)) return;
            
            // Check if we're transitioning from above-the-fold to below-the-fold
            if (lastWasAboveTheFold && task.below_the_fold && !separatorAdded) {
                // Add a separator in the sidebar
                const separatorRow = document.createElement('div');
                separatorRow.className = 'fold-separator';
                separatorRow.innerHTML = '<div class="separator-text">Below The Fold</div>';
                sidebarListEl.appendChild(separatorRow);
                
                // Add a separator in the timeline
                const timelineSeparator = document.createElement('div');
                timelineSeparator.className = 'fold-separator-timeline';
                timelineSeparator.style.width = currentWidth + 'px';
                barsContainerEl.appendChild(timelineSeparator);
                
                // Update visibleIndex to account for the separator
                visibleIndex++;
                
                // Update the flags
                lastWasAboveTheFold = false;
                separatorAdded = true;
            }

            const sideRow = document.createElement('div');
            sideRow.className = task.below_the_fold ? 'task-row below-fold' : 'task-row';
            const indent = task.depth * 20;
            const icon = task.hasChildren ? (task.expanded ? '▼' : '▶') : '&bull;';
            const nameEl = document.createElement('div');
            nameEl.className = 'task-name-container';
            nameEl.style.paddingLeft = (indent + 10) + 'px';
            if (task.hasChildren) {
                nameEl.style.fontWeight = '600';
                nameEl.innerHTML = `<span class="toggle-icon">${icon}</span> ${task.name}`;
                nameEl.onclick = () => { 
                    task.expanded = !task.expanded; 
                    renderRows(); 
                    // Redraw horizontal grid lines after expanding/collapsing
                    drawHorizontalGridLines();
                };
            } else {
                 nameEl.innerHTML = `<span class="toggle-icon" style="opacity:0.3">${icon}</span> ${task.name}`;
            }
            sideRow.appendChild(nameEl);
            sidebarListEl.appendChild(sideRow);

            if (task.start && task.end) {
                const startPct = (task.start - startDate) / totalTime;
                const durPct = (task.end - task.start) / totalTime;
                const left = startPct * currentWidth;
                const width = durPct * currentWidth;
                const top = axisHeight + (visibleIndex * rowHeight);
                
                // Create full-height highlight if the task has highlight_full_height set to true
                if (task.highlight_full_height) {
                    // Create the full-height highlight element
                    const fullHeightHighlight = document.createElement('div');
                    fullHeightHighlight.className = 'gantt-full-height-highlight';
                    fullHeightHighlight.style.left = left + 'px';
                    fullHeightHighlight.style.width = Math.max(width, 2) + 'px';
                    fullHeightHighlight.style.top = axisHeight + 'px';
                    
                    // We'll use CSS to ensure it extends the full height
                    // The height: 100% !important in CSS will make it fill the container
                    
                    // Apply custom color if provided
                    if (task.color && /^#([0-9A-F]{3}){1,2}$/i.test(task.color)) {
                        fullHeightHighlight.style.backgroundColor = task.color + '20'; // Add 12.5% opacity
                        fullHeightHighlight.style.borderLeft = '1px solid ' + task.color + '40'; // Add 25% opacity
                        fullHeightHighlight.style.borderRight = '1px solid ' + task.color + '40'; // Add 25% opacity
                    }
                    
                    barsContainerEl.appendChild(fullHeightHighlight);
                }
                
                // Track parent-child relationships for grouping
                if (task.parentId) {
                    if (!parentGroups[task.parentId]) {
                        parentGroups[task.parentId] = {
                            children: [],
                            minLeft: Infinity,
                            maxRight: -Infinity,
                            minTop: Infinity,
                            maxBottom: -Infinity
                        };
                    }
                    
                    // Add this task to its parent's children
                    parentGroups[task.parentId].children.push({
                        left: left,
                        right: left + width,
                        top: top,
                        bottom: top + rowHeight
                    });
                    
                    // Update parent's boundaries
                    parentGroups[task.parentId].minLeft = Math.min(parentGroups[task.parentId].minLeft, left);
                    parentGroups[task.parentId].maxRight = Math.max(parentGroups[task.parentId].maxRight, left + width);
                    parentGroups[task.parentId].minTop = Math.min(parentGroups[task.parentId].minTop, top);
                    parentGroups[task.parentId].maxBottom = Math.max(parentGroups[task.parentId].maxBottom, top + rowHeight);
                }

                const bar = document.createElement('div');
                bar.className = 'gantt-bar' + (task.hasChildren ? ' parent-bar' : '');
                bar.style.left = left + 'px';
                bar.style.width = Math.max(width, 2) + 'px';
                bar.style.top = (top + 7.5) + 'px'; // Consistent positioning for all bars
                
                // Apply custom color if provided
                if (task.color && /^#([0-9A-F]{3}){1,2}$/i.test(task.color)) {
                    bar.style.backgroundColor = task.color;
                    
                    // For parent bars with custom colors, keep them visible but slightly transparent
                    if (task.hasChildren) {
                        bar.style.opacity = '0.7';
                    }
                }
                
                // Add click handler for expanding/collapsing when clicking on bars
                if (task.hasChildren) {
                    bar.style.cursor = 'pointer';
                    bar.onclick = (e) => {
                        // Prevent tooltip from showing on click
                        e.stopPropagation();
                        tooltipEl.style.display = 'none';
                        
                        // Toggle expanded state
                        task.expanded = !task.expanded;
                        renderRows();
                        drawHorizontalGridLines();
                    };
                }
                
                // Show tooltip on mouseover
                bar.onmousemove = (e) => {
                    e.stopPropagation();
                    tooltipEl.style.display = 'block';
                    tooltipEl.style.left = (e.clientX + 15) + 'px';
                    tooltipEl.style.top = (e.clientY + 15) + 'px';
                    
                    // Use custom hover text if provided, otherwise use default
                    if (task.hover_text) {
                        tooltipEl.innerHTML = task.hover_text;
                    } else {
                        tooltipEl.innerHTML = `<b>${task.name}</b><br>${new Date(task.start).toLocaleString(undefined, {timeZone: 'UTC'})} UTC<br>to<br>${new Date(task.end).toLocaleString(undefined, {timeZone: 'UTC'})} UTC`;
                        
                        // Show color information if custom color is set
                        if (task.color && /^#([0-9A-F]{3}){1,2}$/i.test(task.color)) {
                            tooltipEl.innerHTML += `<br><span style="color:${task.color};font-weight:bold">Color: ${task.color}</span>`;
                        }
                        
                        // Show highlight information if full-height highlight is enabled
                        if (task.highlight_full_height) {
                            tooltipEl.innerHTML += `<br><span style="color:#6366f1;font-weight:bold">Full-height highlight enabled</span>`;
                        }
                        
                        // Show below-the-fold status
                        if (task.below_the_fold) {
                            tooltipEl.innerHTML += `<br><span style="color:#64748b;font-weight:bold">Below the fold</span>`;
                        }
                    }
                    
                    // Add hint for expandable items (always show this)
                    if (task.hasChildren) {
                        tooltipEl.innerHTML += `<br><span style="color:#aaa;font-size:11px">(Click to ${task.expanded ? 'collapse' : 'expand'})</span>`;
                    }
                };
                bar.onmouseleave = () => { tooltipEl.style.display = 'none'; };

                barsContainerEl.appendChild(bar);
            }
            
            visibleIndex++;
        });
        // Create parent activity group boxes
        Object.keys(parentGroups).forEach(parentId => {
            const parentGroup = parentGroups[parentId];
            
            // Only create group boxes for parents with multiple children
            if (parentGroup.children.length > 1) {
                const parentTask = flatTasks.find(t => t.id === parentId);
                
                // Only create group boxes for expanded parents
                if (parentTask && parentTask.expanded) {
                    // Add padding around the group
                    const padding = 5;
                    
                    // Create the group box element
                    const groupBox = document.createElement('div');
                    groupBox.className = 'parent-activity-group with-shadow';
                    groupBox.style.left = (parentGroup.minLeft - padding) + 'px';
                    groupBox.style.top = (parentGroup.minTop - padding) + 'px';
                    groupBox.style.width = (parentGroup.maxRight - parentGroup.minLeft + (padding * 2)) + 'px';
                    groupBox.style.height = (parentGroup.maxBottom - parentGroup.minTop + (padding * 2)) + 'px';
                    
                    // If parent has a color, use a tinted version of that color for the group
                    if (parentTask.color && /^#([0-9A-F]{3}){1,2}$/i.test(parentTask.color)) {
                        // Create a lighter version of the parent color
                        groupBox.style.backgroundColor = parentTask.color + '15'; // Add 15% opacity
                        groupBox.style.borderColor = parentTask.color + '30'; // Add 30% opacity
                    }
                    
                    barsContainerEl.appendChild(groupBox);
                }
            }
        });
        
        canvasEl.style.height = Math.max(axisHeight + (visibleIndex * rowHeight), 300) + 'px';
    }

    // --- ZOOM ENGINE ---
    const applyZoom = (factor, anchorPx) => {
        if (anchorPx === undefined || anchorPx === null) {
            anchorPx = scrollAreaEl.clientWidth / 2;
        }

        // CRITICAL: Calculate exact time at anchor point before zooming
        const oldPixelsPerMS = pixelsPerMS;
        const oldScroll = scrollAreaEl.scrollLeft;
        
        // This is the absolute time (in ms since epoch) at the anchor point
        const timeAtAnchor = startDate + ((oldScroll + anchorPx) / oldPixelsPerMS);
        
        // Calculate new scale with factor
        let newPixelsPerMS = oldPixelsPerMS * factor;
        
        // Clamp to minimum and maximum zoom
        if (newPixelsPerMS < minZoom) newPixelsPerMS = minZoom;
        if (newPixelsPerMS > maxZoom) newPixelsPerMS = maxZoom;
        
        // Safety check: prevent zooming in further if we're already at max zoom
        if (oldPixelsPerMS >= maxZoom && factor > 1.0) {
            newPixelsPerMS = maxZoom;
            // Don't allow further zooming in
            factor = 1.0;
        }
        
        // Calculate how much time will be visible after zoom
        const visibleTimeAfterZoom = scrollAreaEl.clientWidth / newPixelsPerMS;
        
        // If less than 30 minutes would be visible, limit the zoom
        if (visibleTimeAfterZoom < minVisibleTimeSpan) {
            newPixelsPerMS = scrollAreaEl.clientWidth / minVisibleTimeSpan;
            factor = newPixelsPerMS / oldPixelsPerMS;
            console.log('Zoom limited to maintain minimum visible timespan of 30 minutes');
            
            // Show a temporary message to the user
            const minSpanMsg = document.createElement('div');
            minSpanMsg.style.position = 'absolute';
            minSpanMsg.style.top = '50px';
            minSpanMsg.style.left = '50%';
            minSpanMsg.style.transform = 'translateX(-50%)';
            minSpanMsg.style.background = 'rgba(0,0,0,0.7)';
            minSpanMsg.style.color = 'white';
            minSpanMsg.style.padding = '8px 12px';
            minSpanMsg.style.borderRadius = '4px';
            minSpanMsg.style.zIndex = '1000';
            minSpanMsg.style.fontSize = '12px';
            minSpanMsg.style.fontWeight = 'bold';
            minSpanMsg.innerText = 'Maximum zoom reached (30 minute minimum view)';
            document.body.appendChild(minSpanMsg);
            
            // Remove after 2 seconds
            setTimeout(() => {
                document.body.removeChild(minSpanMsg);
            }, 2000);
        }
        
        // Calculate effective zoom factor (may differ from requested factor due to clamping)
        const effectiveFactor = newPixelsPerMS / oldPixelsPerMS;
        
        // Apply new scale
        pixelsPerMS = newPixelsPerMS;
        
        // Resize canvas - CRITICAL: Do this BEFORE setting scroll position
        const newWidth = totalTime * pixelsPerMS;
        canvasEl.style.width = `${newWidth}px`;
        
        // Calculate new scroll position to keep the time at anchor point stable
        // This is the pixel position where our anchor time should be after zooming
        const newPositionForAnchorTime = (timeAtAnchor - startDate) * pixelsPerMS;
        
        // Adjust scroll to keep anchor time at the same screen position
        const newScroll = newPositionForAnchorTime - anchorPx;
        
        // Set scroll position with bounds check
        // Ensure we don't scroll beyond the timeline boundaries
        // Also ensure we don't scroll past the right edge of the canvas
        const maxScroll = Math.max(0, newWidth - scrollAreaEl.clientWidth);
        scrollAreaEl.scrollLeft = Math.max(0, Math.min(newScroll, maxScroll));
        
        // Extra safety: If we're at a very high zoom level, ensure we don't go beyond the original data bounds
        if (pixelsPerMS > 0.01) { // Only apply this at high zoom levels
            const viewportWidthMs = scrollAreaEl.clientWidth / pixelsPerMS;
            const currentViewStartMs = startDate + (scrollAreaEl.scrollLeft / pixelsPerMS);
            const currentViewEndMs = currentViewStartMs + viewportWidthMs;
            
            // If we're showing area outside the original data range, adjust scroll
            if (currentViewStartMs < originalStartDate && currentViewEndMs < originalEndDate) {
                // Too far left, adjust
                const newScrollLeft = (originalStartDate - startDate) * pixelsPerMS;
                scrollAreaEl.scrollLeft = Math.max(0, newScrollLeft);
            } else if (currentViewEndMs > originalEndDate && currentViewStartMs > originalStartDate) {
                // Too far right, adjust
                const newScrollLeft = (originalEndDate - startDate) * pixelsPerMS - scrollAreaEl.clientWidth;
                scrollAreaEl.scrollLeft = Math.max(0, newScrollLeft);
            }
        }

        // Redraw
        refresh();
        
        // Ensure horizontal grid lines are visible after zooming
        drawHorizontalGridLines();
        
        // Return effective factor for potential chaining
        return effectiveFactor;
    };

    // --- Controls ---
    let zoomInBtn = document.getElementById(`zoom-in-${uniqueId}`);
    let zoomOutBtn = document.getElementById(`zoom-out-${uniqueId}`);
    
    zoomInBtn.onclick = () => {
        // Check if zooming in would exceed the minimum timespan limit
        const potentialPixelsPerMS = pixelsPerMS * 1.5;
        const potentialVisibleTime = scrollAreaEl.clientWidth / potentialPixelsPerMS;
        
        // Don't zoom in if it would make less than 30 minutes visible
        if (potentialVisibleTime < minVisibleTimeSpan) {
            console.log('Button zoom limited to maintain minimum visible timespan of 30 minutes');
            
            // Show a temporary message to the user
            const minSpanMsg = document.createElement('div');
            minSpanMsg.style.position = 'absolute';
            minSpanMsg.style.top = '50px';
            minSpanMsg.style.left = '50%';
            minSpanMsg.style.transform = 'translateX(-50%)';
            minSpanMsg.style.background = 'rgba(0,0,0,0.7)';
            minSpanMsg.style.color = 'white';
            minSpanMsg.style.padding = '8px 12px';
            minSpanMsg.style.borderRadius = '4px';
            minSpanMsg.style.zIndex = '1000';
            minSpanMsg.style.fontSize = '12px';
            minSpanMsg.style.fontWeight = 'bold';
            minSpanMsg.innerText = 'Maximum zoom reached (30 minute minimum view)';
            document.body.appendChild(minSpanMsg);
            
            // Remove after 2 seconds
            setTimeout(() => {
                document.body.removeChild(minSpanMsg);
            }, 2000);
            
            return;
        }
        
        const effectiveFactor = applyZoom(1.5);
        // Disable zoom-in button if we've reached max zoom
        zoomInBtn.disabled = (pixelsPerMS >= maxZoom);
        zoomInBtn.style.opacity = zoomInBtn.disabled ? '0.5' : '1';
        zoomOutBtn.disabled = false;
        zoomOutBtn.style.opacity = '1';
    };
    
    zoomOutBtn.onclick = () => {
        const effectiveFactor = applyZoom(0.66);
        // Re-enable zoom-in button if we're no longer at max zoom
        zoomInBtn.disabled = (pixelsPerMS >= maxZoom);
        zoomInBtn.style.opacity = zoomInBtn.disabled ? '0.5' : '1';
        // Disable zoom-out button if we've reached min zoom
        zoomOutBtn.disabled = (pixelsPerMS <= minZoom);
        zoomOutBtn.style.opacity = zoomOutBtn.disabled ? '0.5' : '1';
    };
    document.getElementById(`fit-${uniqueId}`).onclick = () => {
        pixelsPerMS = initialInnerWidth / totalTime;
        refresh();
        scrollAreaEl.scrollLeft = 0;
    };

    // Wheel Zoom
    scrollAreaEl.addEventListener('wheel', (e) => {
        if (e.ctrlKey || e.metaKey) {
            e.preventDefault();
            const rect = scrollAreaEl.getBoundingClientRect();
            const anchorX = e.clientX - rect.left;
            const direction = e.deltaY > 0 ? 0.9 : 1.1;
            
            // Calculate if zooming in would exceed the minimum timespan limit
            if (direction > 1.0) {
                const potentialPixelsPerMS = pixelsPerMS * direction;
                const potentialVisibleTime = scrollAreaEl.clientWidth / potentialPixelsPerMS;
                
                // Don't zoom in if it would make less than 30 minutes visible
                if (potentialVisibleTime < minVisibleTimeSpan) {
                    console.log('Wheel zoom limited to maintain minimum visible timespan of 30 minutes');
                    return;
                }
            }
            
            // Don't zoom in if already at max zoom
            if (direction > 1.0 && pixelsPerMS >= maxZoom) return;
            
            // Don't zoom out if already at min zoom
            if (direction < 1.0 && pixelsPerMS <= minZoom) return;
            
            const effectiveFactor = applyZoom(direction, anchorX);
            
            // Update button states
            zoomInBtn.disabled = (pixelsPerMS >= maxZoom);
            zoomInBtn.style.opacity = zoomInBtn.disabled ? '0.5' : '1';
            zoomOutBtn.disabled = (pixelsPerMS <= minZoom);
            zoomOutBtn.style.opacity = zoomOutBtn.disabled ? '0.5' : '1';
        }
    }, { passive: false });

    // Live Cursor
    scrollAreaEl.addEventListener('mousemove', (e) => {
        const rect = scrollAreaEl.getBoundingClientRect();
        const scrollLeft = scrollAreaEl.scrollLeft;
        const xInsideScroll = e.clientX - rect.left + scrollLeft;
        
        const pct = xInsideScroll / (totalTime * pixelsPerMS);
        const time = startDate + (pct * totalTime);
        const date = new Date(time);
        
        if (pixelsPerMS > 0.01) {
             cursorTimeEl.innerText = date.toLocaleString(undefined, {hour12:false, timeZone: 'UTC'}) + "." + date.getMilliseconds().toString().padStart(3,'0') + " UTC";
        } else {
             cursorTimeEl.innerText = date.toLocaleString(undefined, {hour12:false, timeZone: 'UTC'}) + " UTC";
        }
    });
    
    scrollAreaEl.addEventListener('mouseleave', () => {
        cursorTimeEl.innerText = "--";
    });

    function refresh() {
        // Use requestAnimationFrame to ensure smooth rendering
        requestAnimationFrame(() => {
            drawAxis();
            renderRows();
            drawHorizontalGridLines(); // Add horizontal grid lines
            
            // Update the height of all full-height highlights to match the canvas height
            const fullHeightHighlights = document.querySelectorAll('.gantt-full-height-highlight');
            const canvasHeight = canvasEl.clientHeight;
            fullHeightHighlights.forEach(highlight => {
                // Set the height to extend from the top of the chart (below axis) to the bottom
                highlight.style.height = (canvasHeight - axisHeight) + 'px';
            });
            
            // Make sure sidebar is properly positioned
            const sidebarEl = document.querySelector(`#gantt-${uniqueId} .gantt-sidebar`);
            if (sidebarEl && scrollAreaEl) {
                sidebarEl.style.transform = `translateY(${-scrollAreaEl.scrollTop}px)`;
            }
        });
    }

    // Function to draw horizontal grid lines
    function drawHorizontalGridLines() {
        // Always clear existing horizontal grid lines to avoid duplicates
        const existingHLines = document.querySelectorAll(`.h-grid-line-${uniqueId}`);
        existingHLines.forEach(line => line.remove());
        
        const currentWidth = totalTime * pixelsPerMS;
        const axisHeight = 40;
        const rowHeight = 35;
        let visibleIndex = 0;
        
        // Create a document fragment for better performance
        const fragment = document.createDocumentFragment();
        
        // Track if we've seen a below-the-fold task yet for separator positioning
        let lastWasAboveTheFold = true;
        let separatorAdded = false;
        
        // Draw horizontal grid lines for visible tasks
        flatTasks.forEach(task => {
            if (!shouldShow(task)) return;
            
            // Check if we're transitioning from above-the-fold to below-the-fold
            if (lastWasAboveTheFold && task.below_the_fold && !separatorAdded) {
                // Add a separator grid line
                const separatorLine = document.createElement('div');
                separatorLine.className = `gantt-grid-line-horizontal h-grid-line-${uniqueId} separator-grid-line`;
                separatorLine.style.top = (axisHeight + (visibleIndex * rowHeight)) + 'px';
                separatorLine.style.width = currentWidth + 'px';
                separatorLine.style.borderTop = '2px solid #cbd5e1';
                fragment.appendChild(separatorLine);
                
                // Update visibleIndex to account for the separator
                visibleIndex++;
                
                // Update the flags
                lastWasAboveTheFold = false;
                separatorAdded = true;
            }
            
            // Add horizontal grid line for this row
            const hGridLine = document.createElement('div');
            hGridLine.className = `gantt-grid-line-horizontal h-grid-line-${uniqueId}`;
            hGridLine.style.top = (axisHeight + (visibleIndex * rowHeight)) + 'px';
            hGridLine.style.width = currentWidth + 'px';
            fragment.appendChild(hGridLine);
            
            visibleIndex++;
        });
        
        // Add all grid lines at once for better performance
        gridEl.appendChild(fragment);
    }
    
    // Handle scrolling - both horizontal and vertical
    scrollAreaEl.addEventListener('scroll', () => {
        // Use requestAnimationFrame for both axis drawing and sidebar sync
        // to ensure they happen in the same animation frame
        requestAnimationFrame(() => {
            // Draw axis
            drawAxis();
            
            // Redraw horizontal grid lines to ensure they're visible
            drawHorizontalGridLines();
            
            // Synchronize the sidebar with vertical scrolling
            const sidebarEl = document.querySelector(`#gantt-${uniqueId} .gantt-sidebar`);
            if (sidebarEl) {
                // Use transform instead of top for better performance
                sidebarEl.style.transform = `translateY(${-scrollAreaEl.scrollTop}px)`;
            }
        });
    });
    
    tlHeaderEl.onwheel = (e) => {
        e.preventDefault();
        const direction = e.deltaY > 0 ? 0.9 : 1.1;
        
        // Calculate if zooming in would exceed the minimum timespan limit
        if (direction > 1.0) {
            const potentialPixelsPerMS = pixelsPerMS * direction;
            const potentialVisibleTime = scrollAreaEl.clientWidth / potentialPixelsPerMS;
            
            // Don't zoom in if it would make less than 30 minutes visible
            if (potentialVisibleTime < minVisibleTimeSpan) {
                console.log('Header wheel zoom limited to maintain minimum visible timespan of 30 minutes');
                return;
            }
        }
        
        // Don't zoom in if already at max zoom
        if (direction > 1.0 && pixelsPerMS >= maxZoom) return;
        
        // Don't zoom out if already at min zoom
        if (direction < 1.0 && pixelsPerMS <= minZoom) return;
        
        const effectiveFactor = applyZoom(direction);
        
        // Update button states
        zoomInBtn.disabled = (pixelsPerMS >= maxZoom);
        zoomInBtn.style.opacity = zoomInBtn.disabled ? '0.5' : '1';
        zoomOutBtn.disabled = (pixelsPerMS <= minZoom);
        zoomOutBtn.style.opacity = zoomOutBtn.disabled ? '0.5' : '1';
    };

    // Initial width set
    canvasEl.style.width = `${totalTime * pixelsPerMS}px`;
    
    // Initialize sidebar position
    const sidebarEl = document.querySelector(`#gantt-${uniqueId} .gantt-sidebar`);
    if (sidebarEl) {
        sidebarEl.style.transform = 'translateY(0)';
    }
    
    // Initial button state
    if (zoomInBtn) zoomInBtn.disabled = (pixelsPerMS >= maxZoom);
    if (zoomOutBtn) zoomOutBtn.disabled = (pixelsPerMS <= minZoom);
    
    // Zoom to first 3 hours by default
    const threeHoursInMs = 3 * 60 * 60 * 1000; // 3 hours in milliseconds
    const defaultViewportWidth = scrollAreaEl.clientWidth;
    
    // Calculate the zoom factor needed to show 3 hours
    const zoomFactor = defaultViewportWidth / threeHoursInMs;
    
    // Apply the zoom
    pixelsPerMS = zoomFactor;
    canvasEl.style.width = `${totalTime * pixelsPerMS}px`;
    
    // Find the first activity with a start time
    let firstActivityTime = startDate;
    
    // Create a sorted copy of tasks by start time
    const sortedTasks = [...flatTasks]
        .filter(task => task.start && task.start > 0)
        .sort((a, b) => a.start - b.start);
    
    // Get the first task's start time if available
    if (sortedTasks.length > 0) {
        firstActivityTime = sortedTasks[0].start;
    }
    
    // Scroll to the first activity
    const scrollOffset = (firstActivityTime - startDate) * pixelsPerMS;
    scrollAreaEl.scrollLeft = Math.max(0, scrollOffset);
    
    // Log the scroll position for debugging
    console.log('Initial scroll position:', {
        firstActivityTime: new Date(firstActivityTime).toISOString(),
        startDate: new Date(startDate).toISOString(),
        scrollOffset: scrollOffset,
        pixelsPerMS: pixelsPerMS
    });
    
    // Render the chart
    refresh();
    
    // Log initialization status
    console.log('Gantt initialization complete', {
        'chart dimensions': `${canvasEl.style.width} x ${canvasEl.style.height}`,
        'data items': flatTasks.length,
        'time range': `${new Date(startDate).toISOString()} to ${new Date(endDate).toISOString()}`,
        'pixelsPerMS': pixelsPerMS
    });
    })();
  }, 100); // Short delay to ensure DOM is ready
});