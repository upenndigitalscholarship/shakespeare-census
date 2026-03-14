/**
 * Simple modal controller - vanilla JS replacement for Bootstrap modal
 */
(function(scope) {
    'use strict';

    let backdrop = null;

    function createBackdrop() {
        if (!backdrop) {
            backdrop = document.createElement('div');
            backdrop.className = 'modal-backdrop';
            backdrop.addEventListener('click', function() {
                Modal.hide();
            });
        }
        return backdrop;
    }

    var Modal = {
        show: function(id) {
            const modal = document.getElementById(id);
            if (!modal) return;

            // Create and show backdrop
            backdrop = createBackdrop();
            document.body.appendChild(backdrop);
            document.body.classList.add('modal-open');

            // Trigger reflow for animation
            backdrop.offsetHeight;
            backdrop.classList.add('in');

            // Show modal
            modal.style.display = 'block';
            modal.offsetHeight; // Trigger reflow
            modal.classList.add('in');

            // Handle escape key
            document.addEventListener('keydown', handleEscape);
        },

        hide: function(id) {
            const modalId = id || (document.querySelector('.modal.in') && document.querySelector('.modal.in').id);
            if (!modalId) return;

            const modal = document.getElementById(modalId);
            if (!modal) return;

            modal.classList.remove('in');

            if (backdrop) {
                backdrop.classList.remove('in');
            }

            setTimeout(function() {
                modal.style.display = 'none';
                if (backdrop && backdrop.parentNode) {
                    backdrop.parentNode.removeChild(backdrop);
                }
                backdrop = null;
                document.body.classList.remove('modal-open');
            }, 300);

            document.removeEventListener('keydown', handleEscape);
        },

        load: function(url, targetId) {
            return fetch(url)
                .then(function(response) {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then(function(html) {
                    const modal = document.getElementById(targetId);
                    if (modal) {
                        modal.innerHTML = html;
                    }
                    return html;
                });
        },

        loadAndShow: function(url, targetId) {
            return Modal.load(url, targetId).then(function() {
                Modal.show(targetId);
            });
        }
    };

    function handleEscape(e) {
        if (e.key === 'Escape' || e.keyCode === 27) {
            Modal.hide();
        }
    }

    scope.Modal = Modal;

})(window);
