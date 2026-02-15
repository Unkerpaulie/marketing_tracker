// Simplified Rich Text Editor using ContentEditable
// This provides formatting capabilities without complex CDN dependencies

console.log('Rich text editor script loaded');

class SimpleRichTextEditor {
  constructor(editorId, hiddenInputId) {
    this.editorId = editorId;
    this.hiddenInputId = hiddenInputId;
    this.editorElement = document.getElementById(editorId);
    this.hiddenInput = document.getElementById(hiddenInputId);

    if (!this.editorElement || !this.hiddenInput) {
      console.error('Editor or hidden input not found');
      return;
    }

    this.init();
  }

  init() {
    console.log('Initializing rich text editor:', this.editorId);

    // Set up contenteditable
    this.editorElement.contentEditable = true;
    this.editorElement.spellcheck = true;

    // Restore content from hidden input if available
    if (this.hiddenInput.value) {
      try {
        this.editorElement.innerHTML = this.hiddenInput.value;
      } catch (e) {
        console.warn('Could not restore editor content:', e);
      }
    }

    // Sync content to hidden input on input
    this.editorElement.addEventListener('input', () => this.syncToHiddenInput());
    this.editorElement.addEventListener('change', () => this.syncToHiddenInput());

    // Handle keyboard shortcuts
    this.editorElement.addEventListener('keydown', (e) => this.handleKeydown(e));

    // Prevent default paste behavior and clean it
    this.editorElement.addEventListener('paste', (e) => this.handlePaste(e));

    console.log('Rich text editor initialized successfully');
  }

  handleKeydown(e) {
    // Bold: Ctrl+B or Cmd+B
    if ((e.ctrlKey || e.metaKey) && e.key === 'b') {
      e.preventDefault();
      document.execCommand('bold', false, null);
      this.syncToHiddenInput();
      return;
    }

    // Italic: Ctrl+I or Cmd+I
    if ((e.ctrlKey || e.metaKey) && e.key === 'i') {
      e.preventDefault();
      document.execCommand('italic', false, null);
      this.syncToHiddenInput();
      return;
    }

    // Underline: Ctrl+U or Cmd+U
    if ((e.ctrlKey || e.metaKey) && e.key === 'u') {
      e.preventDefault();
      document.execCommand('underline', false, null);
      this.syncToHiddenInput();
      return;
    }

    // Sync on any change
    setTimeout(() => this.syncToHiddenInput(), 0);
  }

  handlePaste(e) {
    e.preventDefault();

    // Get pasted text
    const text = e.clipboardData.getData('text/plain');

    // Insert as plain text to avoid unwanted formatting
    if (document.queryCommandSupported('insertText')) {
      document.execCommand('insertText', false, text);
    } else {
      document.execCommand('paste', false, text);
    }

    this.syncToHiddenInput();
  }

  syncToHiddenInput() {
    // Store the HTML content in the hidden input
    this.hiddenInput.value = this.editorElement.innerHTML;
  }

  getContent() {
    return this.hiddenInput.value;
  }

  setContent(content) {
    this.editorElement.innerHTML = content;
    this.syncToHiddenInput();
  }

  applyFormat(command, value = null) {
    document.execCommand(command, false, value);
    this.editorElement.focus();
    this.syncToHiddenInput();
  }
}

// Store editor instances globally
window.richTextEditors = {};

// Initialize all rich text editors on page load
function initializeRichTextEditors() {
  console.log('Initializing rich text editors...');

  const editors = document.querySelectorAll('[data-lexical-editor]');
  console.log('Found', editors.length, 'editor(s) to initialize');

  editors.forEach(editorElement => {
    const editorId = editorElement.id;
    const hiddenInputId = editorElement.dataset.lexicalInput;
    if (editorId && hiddenInputId && !window.richTextEditors[editorId]) {
      console.log('Creating editor instance:', editorId);
      window.richTextEditors[editorId] = new SimpleRichTextEditor(editorId, hiddenInputId);
    }
  });
}

// Set up toolbar button handlers
function setupToolbarButtons() {
  console.log('Setting up toolbar buttons...');

  const toolbarButtons = document.querySelectorAll('.lexical-toolbar button');

  toolbarButtons.forEach((button, index) => {
    button.addEventListener('click', (e) => {
      e.preventDefault();

      // Find the associated editor
      const toolbar = button.closest('.lexical-toolbar');
      const wrapper = toolbar.closest('.lexical-editor-wrapper');
      const editor = wrapper.querySelector('[data-lexical-editor]');
      const editorId = editor.id;

      const richEditor = window.richTextEditors[editorId];
      if (!richEditor) return;

      // Apply formatting based on button index
      switch(index) {
        case 0: // Bold
          richEditor.applyFormat('bold');
          break;
        case 1: // Italic
          richEditor.applyFormat('italic');
          break;
        case 2: // Code
          richEditor.applyFormat('formatBlock', '<pre>');
          break;
        case 3: // Line break (just focus back on editor)
          richEditor.editorElement.focus();
          break;
      }
    });
  });
}

// Initialize when DOM is ready
console.log('Document ready state:', document.readyState);

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded event fired');
    initializeRichTextEditors();
    setupToolbarButtons();
  });
} else {
  console.log('DOM already loaded, initializing immediately');
  initializeRichTextEditors();
  setupToolbarButtons();
}

