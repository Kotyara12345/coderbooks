document.addEventListener('DOMContentLoaded', function() {
    let menuBlock = document.querySelector('.nh_menu-content');
    let myBlock = document.querySelector('.nh_menu-list');
    let contentBlock = document.querySelector('.nh_content');
    let bottomContentBlock = document.querySelector('.nh_content-bottom');
    let blockOffset = myBlock.offsetTop;
    menuFixed();
    window.addEventListener("scroll", function() {
        menuFixed();
    });

    function menuFixed() {
        let scrollY = window.scrollY;
        if (menuBlock.clientHeight < contentBlock.clientHeight && window.innerWidth >= 900) {
            if ((scrollY + window.innerHeight) > (myBlock.clientHeight + blockOffset)) {
                console.log(scrollY + window.innerHeight, myBlock.clientHeight + blockOffset);
                myBlock.classList.add("fixed");
            } else {
                myBlock.classList.remove("fixed");
            }
        }
    }

    document.querySelectorAll('.nh_menu-button').forEach(function (itemButton) {
        itemButton.addEventListener('click', function() {
            const toggle = itemButton.dataset.toggle;
            const elemToggle = document.querySelector(toggle);
            elemToggle.classList.toggle('active');
            if (elemToggle.classList.contains('active')) {
                const toggleBackground = document.createElement('div');
                toggleBackground.classList.add('nh_toggle-background');
                if (bottomContentBlock !== null) {
                    bottomContentBlock.prepend(toggleBackground);
                }
            }
            else {
                document.querySelectorAll('.nh_toggle-background').forEach(function(itemBackground) {
                    itemBackground.remove();
                });
            }
        });
    });

    document.addEventListener('click', (event) => {
        if (event.target && event.target.classList.contains("nh_toggle-background")) {
            document.querySelectorAll('.nh_toggle-window.active').forEach(function(itemWindow) {
                itemWindow.classList.remove('active');
            });
            event.target.remove();
        }
    });

    document.querySelectorAll('.js-accordion-title').forEach(function(itemTitle) {
        const accordion = itemTitle.closest('.js-accordion');
        const content = accordion.querySelector('.js-accordion-body')
        itemTitle.addEventListener('click', function () {
            if (accordion.classList.contains('active')) {
                accordion.classList.remove('active');
                content.style.maxHeight = '';
            } else {
                accordion.classList.add('active');
                content.style.maxHeight = `${content.scrollHeight}px`;
            }
        });
    });
});
