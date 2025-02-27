#!/bin/sh

TRIGGER_FILE="/shared/trigger_build"
HUGO_DESTINATION=${HUGO_DESTINATION:-"/shared/generated"}
HUGO_THEME=${HUGO_THEME:-""}
HUGO_BASEURL=${HUGO_BASEURL:-"http://localhost"}

# Initial build
echo "Performing initial build..."
if [ -n "$HUGO_THEME" ]; then
    hugo --destination="$HUGO_DESTINATION" --theme="$HUGO_THEME" --baseURL="$HUGO_BASEURL"
else
    hugo --destination="$HUGO_DESTINATION" --baseURL="$HUGO_BASEURL"
fi

# Watch for changes if enabled
if [ "$HUGO_WATCH" = "true" ]; then
    echo "Watching for changes..."
    
    # Monitor content directory for changes
    while true; do
        if [ -f "$TRIGGER_FILE" ]; then
            echo "Build triggered at $(date)"
            
            # Rebuild the site
            if [ -n "$HUGO_THEME" ]; then
                hugo --destination="$HUGO_DESTINATION" --theme="$HUGO_THEME" --baseURL="$HUGO_BASEURL"
            else
                hugo --destination="$HUGO_DESTINATION" --baseURL="$HUGO_BASEURL"
            fi
            
            # Remove the trigger file
            rm -f "$TRIGGER_FILE"
        fi
        
        # Check every 5 seconds
        sleep 5
    done
else
    echo "Watch mode disabled. Exiting after initial build."
fi