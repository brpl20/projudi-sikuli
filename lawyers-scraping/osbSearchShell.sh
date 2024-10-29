#!/bin/bash

# Function to URL encode a string
urlencode() {
    local string="${1}"
    local strlen=${#string}
    local encoded=""
    local pos c o

    for (( pos=0 ; pos<strlen ; pos++ )); do
        c=${string:$pos:1}
        case "$c" in
            [-_.~a-zA-Z0-9] ) o="${c}" ;;
            * )               printf -v o '%%%02x' "'$c"
        esac
        encoded+="${o}"
    done
    echo "${encoded}"
}

# Step 1: Search for the name
search_oab() {
    local name="$1"
    local encoded_name=$(urlencode "$name")
    local search_response=$(curl -s -X POST "https://cna.oab.org.br/Home/Search" \
        -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" \
        -H "Accept: application/json, text/javascript, */*; q=0.01" \
        -H "Accept-Language: en-US,en;q=0.9" \
        -H "Connection: keep-alive" \
        -H "Content-Type: application/json" \
        -d "{\"IsMobile\":\"false\",\"NomeAdvo\":\"$encoded_name\",\"Insc\":\"\",\"Uf\":\"\",\"TipoInsc\":\"\"}")
    
    echo "$search_response"
}

# Step 2: Extract DetailUrl from search response
extract_detail_url() {
    local search_response="$1"
    local detail_url=$(echo "$search_response" | grep -o '"DetailUrl":"[^"]*"' | cut -d'"' -f4)
    echo "$detail_url"
}

# Step 3: Get detail page
get_detail_page() {
    local detail_url="$1"
    local detail_response=$(curl -s "https://cna.oab.org.br$detail_url" \
        -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" \
        -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" \
        -H "Accept-Language: en-US,en;q=0.9" \
        -H "Connection: keep-alive")
    
    echo "$detail_response"
}

# Step 4: Extract image URL from detail page
extract_image_url() {
    local detail_page="$1"
    local image_url=$(echo "$detail_page" | grep -o 'src="/Content/Upload/Foto/[^"]*"' | cut -d'"' -f2)
    echo "$image_url"
}

# Step 5: Download image
download_image() {
    local image_url="$1"
    local output_file="$2"
    curl -s "https://cna.oab.org.br$image_url" \
        -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" \
        -H "Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8" \
        -H "Accept-Language: en-US,en;q=0.9" \
        -H "Connection: keep-alive" \
        -H "Referer: https://cna.oab.org.br/Home/Search" \
        --output "$output_file"
}

# Main execution
main() {
    local name="$1"
    
    echo "Searching for: $name"
    search_response=$(search_oab "$name")
    
    echo "Search Response:"
    echo "$search_response"
    
    detail_url=$(extract_detail_url "$search_response")
    if [ -z "$detail_url" ]; then
        echo "No DetailUrl found in search response."
        exit 1
    fi
    
    echo "DetailUrl: $detail_url"
    
    echo "Getting detail page..."
    detail_page=$(get_detail_page "$detail_url")
    
    echo "Detail Page (first 500 characters):"
    echo "${detail_page:0:500}"
    
    image_url=$(extract_image_url "$detail_page")
    if [ -z "$image_url" ]; then
        echo "Image URL not found in detail page."
        exit 1
    fi
    
    echo "Image URL: $image_url"
    
    echo "Downloading image..."
    output_file="${name// /_}.jpg"
    download_image "$image_url" "$output_file"
    
    if [ -f "$output_file" ]; then
        echo "Image downloaded successfully: $output_file"
    else
        echo "Failed to download image."
    fi
}

# Check if a name was provided
if [ "$#" -eq 0 ]; then
    echo "Please provide a name to search for."
    echo "Usage: $0 \"Full Name\""
    exit 1
fi

# Run the main function with the provided name
main "$1"