RSS_FEEDS = {
    "all": "https://www.whatdotheyknow.com/feed/search/%20(variety:sent%20OR%20variety:followup_sent%20OR%20variety:response%20OR%20variety:comment)",
    "successful": "https://www.whatdotheyknow.com/feed/search/%20(latest_status:successful%20OR%20latest_status:partially_successful)",
    "unsuccessful": "https://www.whatdotheyknow.com/feed/search/%20(latest_status:rejected%20OR%20latest_status:not_held)",
    "unresolved": "https://www.whatdotheyknow.com/feed/search/%20(latest_status:waiting_response%20OR%20latest_status:waiting_clarification%20OR%20waiting_classification:true%20OR%20latest_status:internal_review%20OR%20latest_status:gone_postal%20OR%20latest_status:error_message%20OR%20latest_status:requires_admin)"
}
