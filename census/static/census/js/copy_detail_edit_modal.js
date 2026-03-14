/**
 * Copy detail edit modal - vanilla JS
 * Handles loading copy details into a modal
 */
document.addEventListener('DOMContentLoaded', function() {
    const copyDataLinks = document.querySelectorAll('.copy_data');

    copyDataLinks.forEach(function(link) {
        link.addEventListener('click', function(ev) {
            ev.preventDefault();
            const url = this.getAttribute('data-form');

            Modal.loadAndShow(url, 'copyModal').then(function() {
                // Close modal when clicking outside the dialog
                document.addEventListener('click', handleOutsideClick);
            });

            return false;
        });
    });
});

function handleOutsideClick(event) {
    const modalDialog = document.querySelector('.modal-dialog');
    const copyModal = document.getElementById('copyModal');

    if (copyModal && modalDialog && !modalDialog.contains(event.target)) {
        Modal.hide('copyModal');
        document.removeEventListener('click', handleOutsideClick);
    }
}
