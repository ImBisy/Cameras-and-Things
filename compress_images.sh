#!/bin/bash

# Image optimization script for Cameras and Things
# Creates WebP thumbnails and optimized versions

set -e

IMG_DIR="/Users/charlieichikowitz/Developer/Cameras and Things/img"
THUMB_DIR="${IMG_DIR}/thumbs"
WEBP_DIR="${IMG_DIR}/webp"

echo "Creating directories..."
mkdir -p "$THUMB_DIR"
mkdir -p "$WEBP_DIR"

# Count total files
total=$(find "$IMG_DIR" -maxdepth 1 -name "*.png" | wc -l)
current=0

echo "Processing $total images..."

for file in "$IMG_DIR"/*.png; do
    [ -f "$file" ] || continue
    
    current=$((current + 1))
    basename=$(basename "$file" .png)
    
    echo "[$current/$total] Processing: $basename"
    
    # Create 400px wide thumbnail (for gallery view)
    # Using sips for macOS
    sips -Z 400 "$file" --out "${THUMB_DIR}/${basename}.png" 2>/dev/null || true
    
    # Create optimized WebP versions
    cwebp -q 85 -resize 400 0 "$file" -o "${WEBP_DIR}/${basename}-thumb.webp" 2>/dev/null || true
    cwebp -q 85 -resize 1200 0 "$file" -o "${WEBP_DIR}/${basename}-1200.webp" 2>/dev/null || true
    cwebp -q 90 "$file" -o "${WEBP_DIR}/${basename}-full.webp" 2>/dev/null || true
    
done

echo ""
echo "Done! Created optimized versions:"
echo "- Thumbnails (400px): ${THUMB_DIR}"
echo "- WebP versions: ${WEBP_DIR}"
echo ""
ls -lh "$WEBP_DIR" | head -20
