function download() {
    gtag('event', 'product_download', {
        'event_category': 'download',
        'event_action': 'product_download',
        'event_label': 'product_download',
        'value': 11
    });
    alert('Thank you!');
}