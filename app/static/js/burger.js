function burgerMenu(selector) {
    let menu = $(selector);
    let button = menu.find('.burger-menu__button');
    let links = menu.find('.burger-menu__link');

    button.on('click', (e) => {
       e.preventDefault();
       toggleMenu();
    });

    links.on('click', () => toggleMenu());

    function toggleMenu() {
        menu.toggleClass('burger-menu__active');
    }
}
burgerMenu('.burger-menu');