tinyMCE.init({
        mode: "none",
        theme: "advanced",
        language: "en",
        theme_advanced_toolbar_location: "top",
        theme_advanced_toolbar_align: "left",
        theme_advanced_statusbar_location: "",
        theme_advanced_buttons1: "formatselect,|,bold,italic,|,bullist,numlist,|,anchor,link,unlink,|,code",
        theme_advanced_buttons2: "",
        theme_advanced_buttons3: "",
        theme_advanced_path: false,
        theme_advanced_blockformats: "p,h2,h3",
        theme_advanced_resizing: true,
        width: '680',
        height: '200',
        plugins: "inlinepopups, paste",
        paste_auto_cleanup_on_paste: true,
        relative_urls: false,
        convert_fonts_to_spans: true
});


function enable_tinymce() {
    $('.tinymce, .inline-related:not(.empty-form) .tinymce').each(function () {
        tinyMCE.execCommand('mceRemoveControl', false, this.id);
        tinyMCE.execCommand('mceAddControl', false, this.id);
    });
}

$(function() {
    // Enable tinymce

    $('div.add-row a').click(enable_tinymce);
    enable_tinymce();
});
