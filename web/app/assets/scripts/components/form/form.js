class ComponentForm {
    static selector = '[data-component-form]';

    selectors = {
        submit: '[data-component-form-child="submit"]',
        validable: '[data-component-form] input:not([type=hidden])',
    };
    children = {
        submit: null,
        validableAll: null,
    };
    options = {
        submitDisabledClass: 'ui-button_disabled',
    };
    root = null;
    valid = false;

    constructor(element) {
        this.root = element;

        this.initChildren();
        this.initValidableAll();

        this.validate();
        // window.addEventListener('ready', this.validate);
    }

    initChildren = () => {
        this.children.submit = this.root.querySelector(this.selectors.submit);
        this.children.validableAll = this.root.querySelectorAll(this.selectors.validable);
    }

    initValidableAll= () => {
        for (let i = 0; i < this.children.validableAll.length; i++) {
            const item = this.children.validableAll[i];
            item.addEventListener('input', this.validate);
        }
    }
    
    validate = () => {
        console.log('Validate');
        for (let i = 0; i < this.children.validableAll.length; i++) {
            const item = this.children.validableAll[i];
            if (item.value.length === 0) {
                this.valid = false;
                break;
            }
            this.valid = true;
        }
        if (this.valid) {
            this.children.submit.classList.remove(this.options.submitDisabledClass);
        } else {
            this.children.submit.classList.add(this.options.submitDisabledClass);
        }
    }
}

export default ComponentForm;