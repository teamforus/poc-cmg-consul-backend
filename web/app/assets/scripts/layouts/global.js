class LayoutGlobal {
    static selector = 'body';

    options = {
        animationEnabledClassName: '__animation-enabled',
        scrollDisabledClassName: '__scroll-disabled',
    };
    root = null;
    scroll = 0;

    fixBody = () => {
        this.scroll = window.pageYOffset;
        this.root.classList.add(this.options.scrollDisabledClassName);
        this.root.style.top = '-' + this.scroll + 'px';
    }

    unfixBody = () => {
        this.root.classList.remove(this.options.scrollDisabledClassName);
        window.scrollTo(0, this.scroll);
        this.root.style.top = 0;
    }

    constructor(element) {
        this.root = element;
        window.addEventListener('load', () => {
            setTimeout(() => {
                this.root.classList.add(this.options.animationEnabledClassName);
            }, 100);
        });
    }
}

export default LayoutGlobal;