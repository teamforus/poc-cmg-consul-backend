
class PageAuth {
    static selector = '[data-page-auth]';

    selectors = {
        login: '[data-page-auth-child="login"]',
        register: '[data-page-auth-child="register"]',
        switcher: '[data-page-auth-child="switcher"]',
    };
    children = {
        login: null,
        register: null,
        switcherAll: null,
    };
    options = {
        wrapperActiveClass: 'page-auth__wrapper_active',
    };
    root = null;

    constructor(element) {
        this.root = element;

        this.initChildren();
        this.initSwitcherAll();
    }

    initChildren = () => {
        this.children.login = this.root.querySelector(this.selectors.login);
        this.children.register = this.root.querySelector(this.selectors.register);
        this.children.switcherAll = this.root.querySelectorAll(this.selectors.switcher);
    }

    initSwitcherAll = () => {
        for (let i = 0; i < this.children.switcherAll.length; i++) {
            const item = this.children.switcherAll[i];
            item.addEventListener('click', this.toggleWrappers);
        }
    }
    toggleWrappers = () => {
        this.children.login.classList.toggle(this.options.wrapperActiveClass);
        this.children.register.classList.toggle(this.options.wrapperActiveClass);
    }
}

export default PageAuth;