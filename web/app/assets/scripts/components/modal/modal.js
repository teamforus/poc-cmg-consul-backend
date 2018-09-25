class ComponentModal {
    static selector = '[data-modal]';

    selectors = {
        open: 'data-modal-open',
        close: 'data-modal-close',
    };
    children = {
        openAll: null,
        closeAll: null,
    };
    options = {
        modalDatasetTitle: 'modal',
        modalActiveClass: 'modal_active',
        modalExitClass: 'modal_exit',
        modalAnimationDuration: 250,
    };
    modal = null;
    root = null;

    constructor(element) {
        this.root = element;
        this.modal = this.root.dataset.modal;

        this.initChildren();
        this.initOpenAll();
        this.initCloseAll();
    }
    initChildren = () => {
        this.children.openAll = document.querySelectorAll(`[${this.selectors.open}="${this.modal}"]`);
        this.children.closeAll = document.querySelectorAll(`[${this.selectors.close}="${this.modal}"]`);
    }
    
    initOpenAll = () => {
        for (let i = 0, l = this.children.openAll.length; i < l; i++) {
            this.children.openAll[i].addEventListener('click', this.open);
        }
    }

    initCloseAll = () => {
        for (let i = 0, l = this.children.closeAll.length; i < l; i++) {
            this.children.closeAll[i].addEventListener('click', this.close);
        }
    }

    open = () => {
        window.app.getComponentInstancesByName('LayoutGlobal')[0].instance.fixBody();
        this.root.classList.add(this.options.modalActiveClass);
    }

    close = () => {
        this.root.classList.add(this.options.modalExitClass);
        window.app.getComponentInstancesByName('LayoutGlobal')[0].instance.unfixBody();

        const toid = setTimeout(() => {
            this.root.classList.remove(this.options.modalExitClass);
            this.root.classList.remove(this.options.modalActiveClass);
            clearTimeout(toid);
        }, this.options.modalAnimationDuration);
    }
}

export default ComponentModal;