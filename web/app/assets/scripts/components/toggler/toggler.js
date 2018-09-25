
class ComponentToggler {
    static selector = '[data-component-toggler]';

    selectors = {
    };
    children = {
        targetAll: null,
    };
    options = {
        class: null,
        selector: null,
    };
    root = null;

    constructor(element) {
        this.root = element;

        
        this.initOptions();
        this.initChildren();
        this.initToggler();
        
    }

    initOptions = () => {
        this.options.selector = `[data-component-toggler-target="${this.root.dataset.componentTogglerTargetValue}"]`;
        this.options.class = this.root.dataset.componentTogglerClass;
    }
    initChildren = () => {
        this.children.targetAll = document.querySelectorAll(this.options.selector);
    }
    initToggler = () => {
        this.root.addEventListener('click', () => {
            for (let i = 0; i < this.children.targetAll.length; i++) {
                this.children.targetAll[i].classList.toggle(this.options.class);
            }
        });
    }
}

export default ComponentToggler;