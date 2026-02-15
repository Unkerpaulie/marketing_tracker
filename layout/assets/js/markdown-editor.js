/**
 * Markdown Editor Initialization
 * Uses EasyMDE for markdown-based rich text editing
 * Stores content as markdown, which is Facebook-compatible
 */

document.addEventListener('DOMContentLoaded', function() {
    // Find all markdown editor textareas
    const editors = document.querySelectorAll('.markdown-editor-input');
    
    editors.forEach(function(textarea) {
        // Initialize EasyMDE for this textarea
        const easyMDE = new EasyMDE({
            element: textarea,
            spellChecker: false,
            autoDownloadFontAwesome: false,
            toolbar: [
                {
                    name: "bold",
                    action: EasyMDE.toggleBold,
                    className: "fa fa-bold",
                    title: "Bold (*text* or **text**)",
                },
                {
                    name: "italic",
                    action: EasyMDE.toggleItalic,
                    className: "fa fa-italic",
                    title: "Italic (_text_ or __text__)",
                },
                {
                    name: "strikethrough",
                    action: EasyMDE.toggleStrikethrough,
                    className: "fa fa-strikethrough",
                    title: "Strikethrough (~text~)",
                },
                "|",
                {
                    name: "quote",
                    action: EasyMDE.toggleBlockquote,
                    className: "fa fa-quote-left",
                    title: "Quote",
                },
                {
                    name: "unordered-list",
                    action: EasyMDE.toggleUnorderedList,
                    className: "fa fa-list-ul",
                    title: "Unordered List",
                },
                {
                    name: "ordered-list",
                    action: EasyMDE.toggleOrderedList,
                    className: "fa fa-list-ol",
                    title: "Ordered List",
                },
                "|",
                {
                    name: "link",
                    action: EasyMDE.drawLink,
                    className: "fa fa-link",
                    title: "Create Link",
                },
                "|",
                {
                    name: "preview",
                    action: EasyMDE.togglePreview,
                    className: "fa fa-eye no-disable",
                    title: "Toggle Preview",
                },
                {
                    name: "side-by-side",
                    action: EasyMDE.toggleSideBySide,
                    className: "fa fa-columns no-disable no-mobile",
                    title: "Toggle Side by Side",
                },
                {
                    name: "fullscreen",
                    action: EasyMDE.toggleFullScreen,
                    className: "fa fa-arrows-alt no-disable no-mobile",
                    title: "Toggle Fullscreen",
                },
                "|",
                {
                    name: "guide",
                    action: "https://www.markdownguide.org/basic-syntax/",
                    className: "fa fa-question-circle",
                    title: "Markdown Guide",
                },
            ],
            status: ["lines", "words", "cursor"],
            initialValue: textarea.value,
            lineNumbers: false,
            lineWrapping: true,
            indentWithTabs: false,
            tabSize: 4,
            indentUnit: 4,
            styleSelectedText: true,
            promptURLs: true,
            forceSync: true,
        });

        // Store reference to editor for potential future use
        textarea.easyMDE = easyMDE;

        // Sync content back to textarea on change
        easyMDE.codemirror.on('change', function() {
            textarea.value = easyMDE.value();
        });

        console.log('EasyMDE editor initialized for:', textarea.id);
    });
});

